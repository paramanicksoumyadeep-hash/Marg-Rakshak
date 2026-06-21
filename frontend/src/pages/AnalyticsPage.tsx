
import { useState } from 'react';
import { ShieldCheck, Crosshair, BrainCircuit, Activity, X } from 'lucide-react';

const AnalyticsPage = () => {
  const [expandedImage, setExpandedImage] = useState<string | null>(null);

  const inferenceImages = [
    { title: 'Training Batch 0', src: '/metrics/train_batch0.jpg' },
    { title: 'Training Batch 1', src: '/metrics/train_batch1.jpg' },
    { title: 'Training Batch 2', src: '/metrics/train_batch2.jpg' },
    { title: 'Training Batch 92600', src: '/metrics/train_batch92600.jpg' },
    { title: 'Training Batch 92601', src: '/metrics/train_batch92601.jpg' },
    { title: 'Training Batch 92602', src: '/metrics/train_batch92602.jpg' },
    { title: 'Val Batch 0 (Truth)', src: '/metrics/val_batch0_labels.jpg' },
    { title: 'Val Batch 0 (Pred)', src: '/metrics/val_batch0_pred.jpg' },
    { title: 'Val Batch 1 (Truth)', src: '/metrics/val_batch1_labels.jpg' },
    { title: 'Val Batch 1 (Pred)', src: '/metrics/val_batch1_pred.jpg' },
    { title: 'Val Batch 2 (Truth)', src: '/metrics/val_batch2_labels.jpg' },
    { title: 'Val Batch 2 (Pred)', src: '/metrics/val_batch2_pred.jpg' }
  ];

  return (
    <div className="max-w-7xl mx-auto mt-6 pb-12 relative">
      <div className="mb-8 flex items-center gap-4">
        <BrainCircuit className="w-10 h-10 text-primary dark:text-red-500" />
        <div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white tracking-tight">Model Evaluation Dashboard</h2>
          <p className="text-gray-500 dark:text-gray-400 mt-1">Eagle Eye v1 (YOLOv8) | Actual Training Metrics (Epoch 50)</p>
        </div>
      </div>

      {/* Top Metrics Row */}
      <div className="grid grid-cols-4 gap-6 mb-8">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400 mb-2 font-medium">
            <ShieldCheck className="w-5 h-5 text-green-500" /> Overall mAP@50
          </div>
          <div className="text-4xl font-black text-gray-900 dark:text-white">71.7%</div>
        </div>
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400 mb-2 font-medium">
            <Crosshair className="w-5 h-5 text-blue-500" /> Precision
          </div>
          <div className="text-4xl font-black text-gray-900 dark:text-white">76.1%</div>
        </div>
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400 mb-2 font-medium">
            <Activity className="w-5 h-5 text-orange-500" /> Recall
          </div>
          <div className="text-4xl font-black text-gray-900 dark:text-white">66.4%</div>
        </div>
        <div className="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700">
          <div className="flex items-center gap-2 text-gray-500 dark:text-gray-400 mb-2 font-medium">
            <BrainCircuit className="w-5 h-5 text-purple-500" /> F1 Score
          </div>
          <div className="text-4xl font-black text-gray-900 dark:text-white">70.9%</div>
        </div>
      </div>

      {/* Middle Row: Confusion Matrix & F1 Curve */}
      <div className="grid grid-cols-2 gap-8 mb-8">
        {/* Confusion Matrix */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-sm border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-gray-200 mb-6">Confusion Matrix (Normalized)</h3>
          <div className="flex justify-center">
            <img src="/metrics/confusion_matrix_normalized.png" alt="Confusion Matrix" className="max-w-full h-auto rounded-xl border border-gray-100 dark:border-gray-700" />
          </div>
        </div>

        {/* F1 Curve */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-sm border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-gray-200 mb-6">F1 Score Curve</h3>
          <div className="flex justify-center">
            <img src="/metrics/BoxF1_curve.png" alt="F1 Curve" className="max-w-full h-auto rounded-xl border border-gray-100 dark:border-gray-700" />
          </div>
        </div>
      </div>

      {/* Bottom Row: PR Curve & Results */}
      <div className="grid grid-cols-2 gap-8">
        {/* Precision-Recall Curve */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-sm border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-gray-200 mb-6">Precision-Recall (PR) Curve</h3>
          <div className="flex justify-center">
            <img src="/metrics/BoxPR_curve.png" alt="PR Curve" className="max-w-full h-auto rounded-xl border border-gray-100 dark:border-gray-700" />
          </div>
        </div>

        {/* Training Results */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-sm border border-gray-200 dark:border-gray-700">
          <h3 className="text-lg font-bold text-gray-800 dark:text-gray-200 mb-6">Training Losses & Metrics</h3>
          <div className="flex justify-center">
            <img src="/metrics/results.png" alt="Results Overview" className="max-w-full h-auto rounded-xl border border-gray-100 dark:border-gray-700" />
          </div>
        </div>
      </div>

      {/* Validation Prediction Batches Row */}
      <div className="mt-12">
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Validation Inference (Actual Predictions)</h3>
        <p className="text-gray-500 dark:text-gray-400 mb-8 font-medium">Click on any image to expand and view the detailed bounding boxes and confidence scores.</p>
        
        <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {inferenceImages.map((img, idx) => (
            <div 
              key={idx} 
              className="bg-white dark:bg-gray-800 p-4 rounded-3xl shadow-sm border border-gray-200 dark:border-gray-700 cursor-pointer group hover:shadow-md transition-all hover:-translate-y-1"
              onClick={() => setExpandedImage(img.src)}
            >
              <h4 className="text-sm font-bold text-gray-800 dark:text-gray-200 mb-3 text-center">{img.title}</h4>
              <div className="relative rounded-xl overflow-hidden aspect-[4/3] bg-gray-100 dark:bg-gray-900 border border-gray-100 dark:border-gray-700">
                <img 
                  src={img.src} 
                  alt={img.title} 
                  className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    // Fallback to empty state if image is missing
                    (e.target as HTMLImageElement).src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 400 300"><rect width="400" height="300" fill="%23f3f4f6"/><text x="50%" y="50%" font-family="sans-serif" font-size="14" fill="%239ca3af" text-anchor="middle" dominant-baseline="middle">Image pending training generation</text></svg>';
                  }}
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/10 transition-colors duration-300 flex items-center justify-center">
                  <span className="opacity-0 group-hover:opacity-100 bg-white/90 text-gray-900 text-xs font-bold px-3 py-1.5 rounded-full shadow-lg transform translate-y-2 group-hover:translate-y-0 transition-all">
                    Click to Enlarge
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Image Modal Overlay */}
      {expandedImage && (
        <div 
          className="fixed inset-0 z-[9999] bg-black/80 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-200"
          onClick={() => setExpandedImage(null)}
        >
          <div className="relative max-w-7xl max-h-[90vh] w-full flex items-center justify-center">
            <button 
              className="absolute -top-12 right-0 md:-right-12 md:top-0 bg-white/10 hover:bg-white/20 text-white p-2 rounded-full transition-colors backdrop-blur-md"
              onClick={(e) => {
                e.stopPropagation();
                setExpandedImage(null);
              }}
            >
              <X size={24} />
            </button>
            <img 
              src={expandedImage} 
              alt="Expanded Validation Image" 
              className="max-w-full max-h-[90vh] object-contain rounded-lg shadow-2xl"
              onClick={(e) => e.stopPropagation()} 
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalyticsPage;
