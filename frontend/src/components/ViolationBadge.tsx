import React from 'react';
import { AlertTriangle, AlertCircle, ShieldAlert, XOctagon } from 'lucide-react';

interface Props {
  type: string;
  className?: string;
}

const formatType = (type: string) => {
  return type.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
};

const getSeverityStyles = (type: string) => {
  switch (type) {
    case 'wrong_side_driving':
    case 'red_light_violation':
      return { bg: 'bg-primary/10', text: 'text-primary', icon: <XOctagon size={16} className="mr-1" /> };
    case 'helmet_non_compliance':
    case 'triple_riding':
    case 'seatbelt_non_compliance':
      return { bg: 'bg-orange-500/10', text: 'text-orange-600', icon: <AlertTriangle size={16} className="mr-1" /> };
    case 'stop_line_violation':
    case 'illegal_parking':
      return { bg: 'bg-yellow-500/10', text: 'text-yellow-600', icon: <AlertCircle size={16} className="mr-1" /> };
    default:
      return { bg: 'bg-gray-100', text: 'text-gray-600', icon: <ShieldAlert size={16} className="mr-1" /> };
  }
};

export const ViolationBadge: React.FC<Props> = ({ type, className = "" }) => {
  const styles = getSeverityStyles(type);
  
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${styles.bg} ${styles.text} ${className}`}>
      {styles.icon}
      {formatType(type)}
    </span>
  );
};
