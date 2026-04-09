import * as React from "react"
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip"

/** Props para o componente DefaultTooltip */
type DefaultTooltipProps = {
  content: React.ReactNode
  children: React.ReactNode

  side?: "top" | "bottom" | "left" | "right"
  align?: "start" | "center" | "end"

  delayDuration?: number
  disableHoverableContent?: boolean

  className?: string
}

/** Tooltip padrão */
export function DefaultTooltip({
  content,
  children,
  side = "top",
  align = "center",
  delayDuration = 200,
  disableHoverableContent = false,
  className,
}: DefaultTooltipProps) {
  return (
    <TooltipProvider delayDuration={delayDuration}>
      <Tooltip disableHoverableContent={disableHoverableContent}>
        <TooltipTrigger asChild>
          {children}
        </TooltipTrigger>

        <TooltipContent
          side={side}
          align={align}
          className={className}
        >
          {content}
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}