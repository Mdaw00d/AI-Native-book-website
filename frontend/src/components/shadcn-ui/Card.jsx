import React from 'react';
import clsx from 'clsx';

/**
 * Card components based on shadcn/ui design
 * Flexible card component for displaying content
 */

const Card = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={clsx(
      'relative rounded-xl overflow-hidden',
      'bg-white/80 dark:bg-gray-900/80',
      'backdrop-blur-lg',
      'border border-[#00D9FF]/20 dark:border-[#00D9FF]/15',
      'shadow-lg hover:shadow-2xl',
      'transition-all duration-300',
      'hover:scale-[1.02] hover:border-[#00D9FF]/40',
      'text-gray-900 dark:text-gray-100',
      'before:absolute before:inset-0 before:rounded-xl',
      'before:bg-gradient-to-br before:from-[#0077FF]/10 before:via-[#00D9FF]/10 before:to-[#00C9A7]/10',
      'before:opacity-0 hover:before:opacity-100 before:transition-opacity before:duration-300',
      'before:pointer-events-none',
      'hover:shadow-[0_0_30px_rgba(0,217,255,0.2)]',
      className
    )}
    {...props}
  />
));
Card.displayName = 'Card';

const CardHeader = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={clsx('relative z-10 flex flex-col space-y-1.5 p-6', className)}
    {...props}
  />
));
CardHeader.displayName = 'CardHeader';

const CardTitle = React.forwardRef(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={clsx(
      'text-2xl font-bold leading-none tracking-tight',
      'bg-gradient-to-r from-[#0077FF] via-[#00D9FF] to-[#00C9A7]',
      'bg-clip-text text-transparent',
      'dark:from-[#00D9FF] dark:via-[#7FD8FF] dark:to-[#00C9A7]',
      className
    )}
    {...props}
  />
));
CardTitle.displayName = 'CardTitle';

const CardDescription = React.forwardRef(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={clsx(
      'text-sm text-gray-700 dark:text-gray-300',
      'font-medium',
      className
    )}
    {...props}
  />
));
CardDescription.displayName = 'CardDescription';

const CardContent = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={clsx(
      'relative z-10 p-6 pt-0',
      'text-gray-800 dark:text-gray-200',
      className
    )}
    {...props}
  />
));
CardContent.displayName = 'CardContent';

const CardFooter = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={clsx(
      'relative z-10 flex items-center p-6 pt-0',
      className
    )}
    {...props}
  />
));
CardFooter.displayName = 'CardFooter';

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent };
