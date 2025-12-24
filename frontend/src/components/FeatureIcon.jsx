import React from 'react';

export default function FeatureIcon({ type, className = '' }) {
  const iconClasses = `w-12 h-12 ${className}`;

  const gradientId = `gradient-${type}`;

  const icons = {
    code: (
      <svg className={iconClasses} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#0077FF', stopOpacity: 1 }} />
            <stop offset="50%" style={{ stopColor: '#00D9FF', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#00C9A7', stopOpacity: 1 }} />
          </linearGradient>
        </defs>
        <path
          d="M16 18L22 12L16 6M8 6L2 12L8 18"
          stroke={`url(#${gradientId})`}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
    diagram: (
      <svg className={iconClasses} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#00D9FF', stopOpacity: 1 }} />
            <stop offset="50%" style={{ stopColor: '#00C9A7', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#7FD8FF', stopOpacity: 1 }} />
          </linearGradient>
        </defs>
        <rect x="3" y="3" width="7" height="7" rx="1" stroke={`url(#${gradientId})`} strokeWidth="2" fill={`url(#${gradientId})`} fillOpacity="0.2" />
        <rect x="14" y="3" width="7" height="7" rx="1" stroke={`url(#${gradientId})`} strokeWidth="2" fill={`url(#${gradientId})`} fillOpacity="0.2" />
        <rect x="14" y="14" width="7" height="7" rx="1" stroke={`url(#${gradientId})`} strokeWidth="2" fill={`url(#${gradientId})`} fillOpacity="0.2" />
        <rect x="3" y="14" width="7" height="7" rx="1" stroke={`url(#${gradientId})`} strokeWidth="2" fill={`url(#${gradientId})`} fillOpacity="0.2" />
      </svg>
    ),
    robot: (
      <svg className={iconClasses} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#0077FF', stopOpacity: 1 }} />
            <stop offset="50%" style={{ stopColor: '#00D9FF', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#7FD8FF', stopOpacity: 1 }} />
          </linearGradient>
        </defs>
        <rect x="5" y="11" width="14" height="10" rx="2" stroke={`url(#${gradientId})`} strokeWidth="2" fill={`url(#${gradientId})`} fillOpacity="0.2" />
        <circle cx="9" cy="16" r="1" fill={`url(#${gradientId})`} />
        <circle cx="15" cy="16" r="1" fill={`url(#${gradientId})`} />
        <rect x="10" y="7" width="4" height="4" rx="1" stroke={`url(#${gradientId})`} strokeWidth="2" fill={`url(#${gradientId})`} fillOpacity="0.2" />
        <path d="M12 7V4" stroke={`url(#${gradientId})`} strokeWidth="2" strokeLinecap="round" />
      </svg>
    ),
    sparkle: (
      <svg className={iconClasses} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#7FD8FF', stopOpacity: 1 }} />
            <stop offset="50%" style={{ stopColor: '#00C9A7', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#00D9FF', stopOpacity: 1 }} />
          </linearGradient>
        </defs>
        <path
          d="M12 2L13.5 8.5L20 10L13.5 11.5L12 18L10.5 11.5L4 10L10.5 8.5L12 2Z"
          stroke={`url(#${gradientId})`}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill={`url(#${gradientId})`}
          fillOpacity="0.3"
        />
        <path
          d="M18 16L18.5 18.5L21 19L18.5 19.5L18 22L17.5 19.5L15 19L17.5 18.5L18 16Z"
          stroke={`url(#${gradientId})`}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill={`url(#${gradientId})`}
          fillOpacity="0.3"
        />
      </svg>
    ),
    book: (
      <svg className={iconClasses} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#00D9FF', stopOpacity: 1 }} />
            <stop offset="50%" style={{ stopColor: '#0077FF', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#00C9A7', stopOpacity: 1 }} />
          </linearGradient>
        </defs>
        <path
          d="M4 19.5C4 18.837 4.26339 18.2011 4.73223 17.7322C5.20107 17.2634 5.83696 17 6.5 17H20"
          stroke={`url(#${gradientId})`}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M6.5 3H20V21H6.5C5.83696 21 5.20107 20.7366 4.73223 20.2678C4.26339 19.7989 4 19.163 4 18.5V5.5C4 4.83696 4.26339 4.20107 4.73223 3.73223C5.20107 3.26339 5.83696 3 6.5 3Z"
          stroke={`url(#${gradientId})`}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill={`url(#${gradientId})`}
          fillOpacity="0.2"
        />
        <path d="M8 7H16M8 11H16M8 15H12" stroke={`url(#${gradientId})`} strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
    refresh: (
      <svg className={iconClasses} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#0077FF', stopOpacity: 1 }} />
            <stop offset="50%" style={{ stopColor: '#00C9A7', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#7FD8FF', stopOpacity: 1 }} />
          </linearGradient>
        </defs>
        <path
          d="M1 4V10H7"
          stroke={`url(#${gradientId})`}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M23 20V14H17"
          stroke={`url(#${gradientId})`}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d="M20.49 9C19.9828 7.56678 19.1209 6.28536 17.9845 5.27542C16.8482 4.26548 15.4745 3.55976 13.9917 3.22426C12.5089 2.88875 10.9652 2.93434 9.50481 3.35677C8.04437 3.77921 6.71475 4.56471 5.64 5.64L1 10M23 14L18.36 18.36C17.2853 19.4353 15.9556 20.2208 14.4952 20.6432C13.0348 21.0657 11.4911 21.1112 10.0083 20.7757C8.52547 20.4402 7.1518 19.7345 6.01547 18.7246C4.87913 17.7146 4.01717 16.4332 3.51 15"
          stroke={`url(#${gradientId})`}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    ),
    eye: (
      <svg className={iconClasses} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#0077FF', stopOpacity: 1 }} />
            <stop offset="50%" style={{ stopColor: '#00D9FF', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#00C9A7', stopOpacity: 1 }} />
          </linearGradient>
        </defs>
        <path
          d="M1 12C1 12 5 4 12 4C19 4 23 12 23 12C23 12 19 20 12 20C5 20 1 12 1 12Z"
          stroke={`url(#${gradientId})`}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill={`url(#${gradientId})`}
          fillOpacity="0.2"
        />
        <circle
          cx="12"
          cy="12"
          r="3"
          stroke={`url(#${gradientId})`}
          strokeWidth="2"
          fill={`url(#${gradientId})`}
          fillOpacity="0.3"
        />
      </svg>
    ),
    brain: (
      <svg className={iconClasses} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#00D9FF', stopOpacity: 1 }} />
            <stop offset="50%" style={{ stopColor: '#00C9A7', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#7FD8FF', stopOpacity: 1 }} />
          </linearGradient>
        </defs>
        <path
          d="M9.5 2C8.96957 2 8.46086 2.21071 8.08579 2.58579C7.71071 2.96086 7.5 3.46957 7.5 4C6.43913 4 5.42172 4.42143 4.67157 5.17157C3.92143 5.92172 3.5 6.93913 3.5 8C2.96957 8 2.46086 8.21071 2.08579 8.58579C1.71071 8.96086 1.5 9.46957 1.5 10C1.5 10.5304 1.71071 11.0391 2.08579 11.4142C2.46086 11.7893 2.96957 12 3.5 12V17C3.5 17.7956 3.81607 18.5587 4.37868 19.1213C4.94129 19.6839 5.70435 20 6.5 20C7.05 20 7.54 19.83 7.96 19.55C8.5 20.45 9.44 21.07 10.5 21.21V22H13.5V21.21C14.56 21.07 15.5 20.45 16.04 19.55C16.46 19.83 16.95 20 17.5 20C18.2956 20 19.0587 19.6839 19.6213 19.1213C20.1839 18.5587 20.5 17.7956 20.5 17V12C21.0304 12 21.5391 11.7893 21.9142 11.4142C22.2893 11.0391 22.5 10.5304 22.5 10C22.5 9.46957 22.2893 8.96086 21.9142 8.58579C21.5391 8.21071 21.0304 8 20.5 8C20.5 6.93913 20.0786 5.92172 19.3284 5.17157C18.5783 4.42143 17.5609 4 16.5 4C16.5 3.46957 16.2893 2.96086 15.9142 2.58579C15.5391 2.21071 15.0304 2 14.5 2H9.5Z"
          stroke={`url(#${gradientId})`}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          fill={`url(#${gradientId})`}
          fillOpacity="0.2"
        />
        <path d="M12 6V10M9 8H15" stroke={`url(#${gradientId})`} strokeWidth="2" strokeLinecap="round" />
      </svg>
    ),
    gear: (
      <svg className={iconClasses} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style={{ stopColor: '#0077FF', stopOpacity: 1 }} />
            <stop offset="50%" style={{ stopColor: '#00D9FF', stopOpacity: 1 }} />
            <stop offset="100%" style={{ stopColor: '#7FD8FF', stopOpacity: 1 }} />
          </linearGradient>
        </defs>
        <circle cx="12" cy="12" r="3" stroke={`url(#${gradientId})`} strokeWidth="2" fill={`url(#${gradientId})`} fillOpacity="0.3" />
        <path
          d="M12 1V4M12 20V23M4.22 4.22L6.34 6.34M17.66 17.66L19.78 19.78M1 12H4M20 12H23M4.22 19.78L6.34 17.66M17.66 6.34L19.78 4.22"
          stroke={`url(#${gradientId})`}
          strokeWidth="2"
          strokeLinecap="round"
        />
      </svg>
    ),
  };

  return (
    <div className="relative inline-block">
      <div className="absolute inset-0 bg-gradient-to-br from-[#0077FF]/20 via-[#00D9FF]/20 to-[#00C9A7]/20 rounded-xl blur-lg"></div>
      <div className="relative bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm p-3 rounded-xl border border-[#00D9FF]/30 shadow-lg shadow-[0_0_15px_rgba(0,217,255,0.2)]">
        {icons[type] || icons.sparkle}
      </div>
    </div>
  );
}
