import React from 'react';
import clsx from 'clsx';

/**
 * Button component based on shadcn/ui design
 * A versatile button component with multiple variants
 */
const Button = React.forwardRef(({
  className,
  variant = 'default',
  size = 'default',
  children,
  ...props
}, ref) => {
  const baseStyles = 'inline-flex items-center justify-center rounded-xl font-semibold transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-[#00D9FF] disabled:pointer-events-none disabled:opacity-50 backdrop-blur-md shadow-lg hover:shadow-2xl hover:scale-105 active:scale-95';

  const variants = {
    default: 'bg-gradient-to-r from-[#0077FF] via-[#00D9FF] to-[#00C9A7] text-white border border-[#00D9FF]/30 hover:border-[#00D9FF]/50 dark:from-[#0077FF] dark:via-[#00D9FF] dark:to-[#7FD8FF] shadow-[0_0_20px_rgba(0,217,255,0.3)] hover:shadow-[0_0_30px_rgba(0,217,255,0.5)]',
    outline: 'border-2 border-[#00D9FF] bg-white/20 backdrop-blur-md text-gray-900 hover:bg-[#00D9FF]/10 dark:text-white dark:border-[#00D9FF] dark:hover:bg-[#00D9FF]/10 shadow-[0_0_15px_rgba(0,119,255,0.2)]',
    ghost: 'border border-transparent bg-white/10 backdrop-blur-sm hover:bg-[#00D9FF]/20 text-gray-900 dark:text-white hover:border-[#00D9FF]/20',
    link: 'border-transparent bg-transparent text-[#0077FF] underline-offset-4 hover:underline dark:text-[#00D9FF] shadow-none hover:shadow-none',
  };

  const sizes = {
    default: 'h-10 px-6 py-2 text-sm',
    sm: 'h-9 px-4 text-xs',
    lg: 'h-12 px-8 text-base',
    icon: 'h-10 w-10',
  };

  return (
    <button
      className={clsx(
        baseStyles,
        variants[variant],
        sizes[size],
        className
      )}
      ref={ref}
      {...props}
    >
      {children}
    </button>
  );
});

Button.displayName = 'Button';

export { Button };
