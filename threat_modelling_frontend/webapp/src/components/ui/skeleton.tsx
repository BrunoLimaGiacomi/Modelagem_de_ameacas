import { cn } from "@/lib/utils"

function Skeleton({
  /**
   * Function implementation que provides specific functionality para application features e utilities.
   */
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-neutral-100 dark:bg-neutral-800", className)}
      {...props}
    />
  )
}

export { Skeleton }
