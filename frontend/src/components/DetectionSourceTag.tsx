import React from 'react';
import { Cpu, Zap, Beaker } from 'lucide-react';

interface Props {
  source: string;
  confidence?: number;
  className?: string;
}

export const DetectionSourceTag: React.FC<Props> = ({ source, confidence, className = "" }) => {
  let icon = <Cpu size={14} className="mr-1" />;
  let color = "bg-blue-100 text-blue-700 border-blue-200";
  
  if (source === 'heuristic') {
    icon = <Zap size={14} className="mr-1" />;
    color = "bg-purple-100 text-purple-700 border-purple-200";
  } else if (source === 'simulated') {
    icon = <Beaker size={14} className="mr-1" />;
    color = "bg-gray-100 text-gray-600 border-gray-200";
  }

  return (
    <div className={`inline-flex items-center px-2 py-0.5 rounded-full border text-[11px] font-semibold tracking-wide uppercase ${color} ${className}`}>
      {icon}
      <span>{source}</span>
      {confidence !== undefined && (
        <span className="ml-1.5 pl-1.5 border-l border-current opacity-80">
          {(confidence * 100).toFixed(1)}%
        </span>
      )}
    </div>
  );
};
