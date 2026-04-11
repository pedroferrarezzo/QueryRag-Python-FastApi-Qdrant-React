import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent } from "@/components/ui/card"
import { Upload, X } from "lucide-react"
import { useAppContext } from "@/contexts/AppContext"
import { toast } from "sonner"
import { ingestVectors } from "@/lib/api"

/** Componente de Upload de Arquivo */
export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const {isLoading, setIsLoading } = useAppContext();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0]
    if (selected) {
      setFile(selected)
    }
  }

  const handleRemove = () => {
    setFile(null)
  }

  const handleUpload = async () => {
    if (!file) return

    try {
        setIsLoading(true);

        await ingestVectors({ file });

        setFile(null);
    }
    catch(err: any) {
        toast.error(err.message || "Erro desconhecido durante o upload do arquivo para ingestão de vetores");
    }
    finally {
      setIsLoading(false)
    }    
  }

  return (
    <Card className="w-full max-w-md">
      <CardContent className="flex flex-col gap-4 p-4">
        <Input
          type="file"
          onChange={handleFileChange}
          disabled={isLoading}
        />

        {file && (
          <div className="flex items-center justify-between rounded-md border p-2 text-sm">
            <span className="truncate">{file.name}</span>
            <button onClick={handleRemove}>
              <X className="h-4 w-4" />
            </button>
          </div>
        )}

        <Button
          onClick={handleUpload}
          disabled={!file || isLoading}
          className="flex items-center gap-2"
        >
          <Upload className="h-4 w-4" />
          {isLoading ? "Enviando..." : "Enviar"}
        </Button>
      </CardContent>
    </Card>
  )
}