import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"
import { Menu } from "lucide-react"
import { Link } from "react-router-dom"
import { HOME_ROUTE, INGEST_VECTOR_ROUTE, SEARCH_VECTOR_ROUTE } from "@/config/routes"

/** Componente de Menu de Navegação */
export function NavigationMenu() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button variant="ghost" size="icon">
          <Menu />
        </Button>
      </SheetTrigger>

      <SheetContent side="left">
        <nav className="flex flex-col gap-4 mt-6">
          <Link to={HOME_ROUTE}>Chat</Link>
          <Link to={INGEST_VECTOR_ROUTE}>Inserir Vetores</Link>
          <Link to={SEARCH_VECTOR_ROUTE}>Pesquisar Vetores</Link>
        </nav>
      </SheetContent>
    </Sheet>
  )
}