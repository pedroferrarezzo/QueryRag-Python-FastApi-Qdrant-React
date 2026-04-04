import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Check, Copy } from "lucide-react"
import { toast } from "sonner"

/** Props para Clipboard */
interface ClipboardProps {
  value: string
  className?: string
}

/** Componente Clipboard para copiar texto para a área de transferência */
export function Clipboard({ value, className }: ClipboardProps) {
  const [copied, setCopied] = useState(false)

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(value)
      setCopied(true)

      toast.success("Copiado para a área de transferência")

      setTimeout(() => setCopied(false), 1500)
    } catch {
      toast.error("Erro ao copiar")
    }
  }

  return (
    <Button
      variant="outline"
      size="icon"
      onClick={handleCopy}
      className={className}
      disabled={copied}
    >
      {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
    </Button>
  )
}