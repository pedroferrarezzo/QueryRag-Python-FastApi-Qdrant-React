import { Loader2 } from "lucide-react";

/** Props para Spinner de Carregamento */
type SpinnerLoadingProps = {
    text: string;
}

/** Componente de Spinner de Carregamento */
export default function SpinnerLoading({ text }: SpinnerLoadingProps) {
    return (
        <div className="flex flex-col items-center justify-center">
            <Loader2 className="h-10 w-10 animate-spin text-muted-foreground" />
            <p className="mt-4 text-sm text-muted-foreground text-center max-w-sm">{text}</p>
        </div>
    )
}