import os
import argparse
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description="Eagle's Eye Model Training")
    parser.add_argument("--epochs", type=int, default=50, help="Number of training epochs")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--model", type=str, default="yolov10n.pt", help="Base model to fine-tune")
    
    args = parser.parse_args()
    
    data_yaml = os.path.abspath("datasets/merged_dataset/merged_data.yaml")
    
    if not os.path.exists(data_yaml):
        print(f"Error: {data_yaml} not found!")
        print("Please run 'python prepare_data.py' first to merge the datasets.")
        return
        
    print(f"Starting training on {data_yaml} for {args.epochs} epochs...")
    
    # Load base model
    model = YOLO(args.model)
    
    # Start training with parameters optimized for accuracy
    results = model.train(
        data=data_yaml,
        epochs=args.epochs,
        batch=args.batch,
        imgsz=640,
        project="weights",
        name="eagle_eye_v1",
        exist_ok=True,
        patience=25,          # Early stopping to prevent overfitting
        workers=8,            # Linux optimization: faster data loading (adjust based on your CPU cores)
        optimizer='auto',     # Automatically selects the best optimizer (SGD or AdamW)
        augment=True          # Enables default YOLO data augmentations to improve generalization
    )
    
    print("Training complete! Best weights saved to weights/eagle_eye_v1/weights/best.pt")

if __name__ == "__main__":
    main()
