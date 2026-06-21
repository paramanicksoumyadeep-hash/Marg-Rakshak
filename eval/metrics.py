from typing import List, Dict
import numpy as np

class EvaluationHarness:
    def __init__(self, iou_threshold: float = 0.5):
        self.iou_threshold = iou_threshold
        # Stores tuples of (pred_bbox, conf, pred_class, gt_bbox, gt_class, is_tp)
        self.matches = []
        self.classes = set()

    def compute_iou(self, boxA: List[int], boxB: List[int]) -> float:
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        interArea = max(0, xB - xA) * max(0, yB - yA)
        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

        if float(boxAArea + boxBArea - interArea) == 0:
            return 0.0
            
        return interArea / float(boxAArea + boxBArea - interArea)

    def add_batch(self, predictions: List[Dict], ground_truths: List[Dict]):
        """
        Adds a batch of predictions and GTs for a single frame.
        Dictionaries expect: 'bbox', 'class_name', 'confidence' (for pred)
        """
        for gt in ground_truths:
            self.classes.add(gt['class_name'])
            
        for pred in predictions:
            self.classes.add(pred['class_name'])

        # Simple greedy matching
        matched_gt_indices = set()
        for pred in sorted(predictions, key=lambda x: x.get('confidence', 0), reverse=True):
            best_iou = 0
            best_gt_idx = -1
            
            for i, gt in enumerate(ground_truths):
                if i in matched_gt_indices:
                    continue
                if pred['class_name'] != gt['class_name']:
                    continue
                    
                iou = self.compute_iou(pred['bbox'], gt['bbox'])
                if iou > best_iou:
                    best_iou = iou
                    best_gt_idx = i
                    
            if best_iou >= self.iou_threshold:
                matched_gt_indices.add(best_gt_idx)
                self.matches.append((pred, ground_truths[best_gt_idx], True))
            else:
                self.matches.append((pred, None, False)) # False positive

        # False negatives (unmatched GTs)
        for i, gt in enumerate(ground_truths):
            if i not in matched_gt_indices:
                self.matches.append((None, gt, False)) # False negative

    def compute_metrics(self) -> Dict[str, Dict[str, float]]:
        metrics = {}
        
        for cls in self.classes:
            tp = sum(1 for p, g, is_tp in self.matches if is_tp and p['class_name'] == cls)
            # FP: Has prediction for cls, but is not TP
            fp = sum(1 for p, g, is_tp in self.matches if p is not None and not is_tp and p['class_name'] == cls)
            # FN: Has GT for cls, but no matching prediction
            fn = sum(1 for p, g, is_tp in self.matches if g is not None and not is_tp and g['class_name'] == cls)
            
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            
            metrics[cls] = {
                "precision": precision,
                "recall": recall,
                "f1": f1,
                "tp": tp,
                "fp": fp,
                "fn": fn
            }
            
        # Global metrics
        total_tp = sum(m['tp'] for m in metrics.values())
        total_fp = sum(m['fp'] for m in metrics.values())
        total_fn = sum(m['fn'] for m in metrics.values())
        
        g_prec = total_tp / (total_tp + total_fp) if (total_tp + total_fp) > 0 else 0.0
        g_rec = total_tp / (total_tp + total_fn) if (total_tp + total_fn) > 0 else 0.0
        g_f1 = 2 * (g_prec * g_rec) / (g_prec + g_rec) if (g_prec + g_rec) > 0 else 0.0
        
        metrics['macro_avg'] = {
            "precision": g_prec,
            "recall": g_rec,
            "f1": g_f1
        }
        
        return metrics
