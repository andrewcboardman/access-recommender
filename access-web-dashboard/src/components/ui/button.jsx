import React from 'react';

export function Button({ className = '', variant, ...props }) {
  const base = 'rounded font-medium transition-colors';
  const styles = variant === 'outline'
    ? 'border border-gray-400 text-gray-800 hover:bg-gray-100'
    : 'bg-black text-white hover:bg-gray-800';
  return <button className={`${base} ${styles} ${className}`} {...props} />;
}
