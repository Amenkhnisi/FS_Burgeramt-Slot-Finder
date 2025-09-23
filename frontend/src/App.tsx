import { Outlet } from 'react-router-dom'
import './App.css'
import NavBar from './components/ui/navBar'

function App() {

  return (

    <div className="felx flex-col justify-center  h-lvh w-full bg-white backdrop-blur-md">
      <NavBar />
      <Outlet />
    </div>

  )
}

export default App
