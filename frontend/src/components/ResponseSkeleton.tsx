import { Skeleton } from "./ui/skeleton";

/** Componente de Skeleton para Respostas */
export default function ResponseSkeleton() {
    return (<div className="space-y-3">
                    <Skeleton className="h-5 w-1/3" />
                    <div className="space-y-2">
                        <Skeleton className="h-4 w-full" />
                        <Skeleton className="h-4 w-[90%]" />
                        <Skeleton className="h-4 w-[80%]" />
                        <Skeleton className="h-4 w-[60%]" />
                    </div>
                </div>)
}