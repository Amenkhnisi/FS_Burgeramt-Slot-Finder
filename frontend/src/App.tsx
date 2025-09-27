import { Outlet } from 'react-router-dom'
import './App.css'
import NavBar from './components/ui/navBar'
import { SpeedInsights } from "@vercel/speed-insights/react"


function App() {

  return (

    <div className="felx flex-col justify-center  h-lvh w-full bg-white backdrop-blur-md">
      <NavBar />
      <Outlet />
      <SpeedInsights />
    </div>

  )
}

export default App
