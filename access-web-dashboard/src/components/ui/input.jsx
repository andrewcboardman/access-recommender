import React from 'react';

export function Input({ className = '', ...props }) {
  return (
    <input
      className={`border border-gray-300 rounded p-2 w-full focus:outline-none focus:ring-2 focus:ring-black ${className}`}
      {...props}
    />
  );
}
