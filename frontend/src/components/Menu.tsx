import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from "@/components/ui/sheet"
import { Button } from "@/components/ui/button"
import { Menu, MessageCircle, Layers, Search } from "lucide-react"
import { Link } from "react-router-dom"
import { HOME_ROUTE, INGEST_VECTOR_ROUTE, SEARCH_VECTOR_ROUTE } from "@/config/routes"
import queryRagLogo from '../assets/query-reg-logo.png';

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
        <SheetHeader className="flex items-center">
          <SheetTitle>
            <img 
                  src={queryRagLogo} 
                  alt="Descrição" 
                  className="h-[clamp(55px,8vw,85px)] w-auto"
              />
          </SheetTitle>
          <SheetDescription>
            Bem vindo ao QueryRag
          </SheetDescription>
        </SheetHeader>
        <nav className="flex flex-col gap-4 mt-6 p-4">
          <Button asChild variant="outline" className="justify-start border-0">
            <Link to={HOME_ROUTE}>
              <MessageCircle />
              Chat
            </Link>
          </Button>
          
          <Button asChild variant="outline" className="justify-start border-0">
            <Link to={INGEST_VECTOR_ROUTE}>
              <Layers />
              Inserir Vetores
            </Link>
          </Button>
          
          <Button asChild variant="outline" className="justify-start border-0">
            <Link to={SEARCH_VECTOR_ROUTE}>
              <Search />
              Pesquisar Vetores
            </Link>
          </Button>
        </nav>
      </SheetContent>
    </Sheet>
  )
}