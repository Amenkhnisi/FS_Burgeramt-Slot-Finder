import React from 'react';
import berlin from "../../assets/berlin.jpg"
import { Link } from 'react-router-dom';

const LandingPage: React.FC = () => {
    return (
        <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-indigo-200 dark:from-gray-900 dark:to-gray-800 text-gray-800 dark:text-gray-100 font-sans">
            {/* Hero Section */}
            <section className="flex flex-col md:flex-row items-center justify-between px-6 md:px-20 py-20 transition-all duration-700 ease-in-out">
                <div className="md:w-1/2 mb-10 md:mb-0 animate-fadeInLeft">
                    <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight drop-shadow-lg">
                        Bürgeramt Slot Finder
                    </h1>
                    <p className="text-lg md:text-xl mb-8 opacity-80 animate-fadeIn">
                        Finden Sie schnell und einfach verfügbare Termine beim Bürgeramt.
                    </p>
                    <Link to={"dashboard"} >
                        <button className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transform hover:scale-105 transition duration-500 shadow-lg">
                            Termin suchen
                        </button>
                    </Link>
                </div>
                <div className="md:w-1/2 animate-fadeInRight">
                    <img src={berlin} alt="Bürgeramt Illustration" className="p-2 rounded-xl shadow-2xl hover:scale-105 transform transition duration-700" />
                </div>
            </section>

            {/* Features Section */}
            <section className="px-6 md:px-20 py-20 bg-white dark:bg-gray-900 rounded-t-3xl">
                <h2 className="text-3xl font-bold mb-12 text-center animate-fadeInUp">Funktionen</h2>
                <div className="grid md:grid-cols-3 gap-10">
                    <div className="p-6 bg-indigo-50 dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-2xl transition transform hover:-translate-y-2 duration-500">
                        <h3 className="font-semibold text-xl mb-4">Schnell Finden</h3>
                        <p>In Sekundenschnelle freie Termine beim Bürgeramt anzeigen lassen.</p>
                    </div>
                    <div className="p-6 bg-indigo-50 dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-2xl transition transform hover:-translate-y-2 duration-500">
                        <h3 className="font-semibold text-xl mb-4">Benachrichtigungen</h3>
                        <p>Lassen Sie sich informieren, sobald neue Termine verfügbar sind.</p>
                    </div>
                    <div className="p-6 bg-indigo-50 dark:bg-gray-800 rounded-2xl shadow-lg hover:shadow-2xl transition transform hover:-translate-y-2 duration-500">
                        <h3 className="font-semibold text-xl mb-4">Benutzerfreundlich</h3>
                        <p>Einfache Oberfläche für eine reibungslose Terminbuchung.</p>
                    </div>
                </div>
            </section>

            {/* Call to Action */}
            <section className="px-6 md:px-20 py-20 text-center">
                <h2 className="text-3xl md:text-4xl font-bold mb-6 animate-fadeInUp">Bereit loszulegen?</h2>
                <p className="mb-8 opacity-90 animate-fadeIn">Starten Sie jetzt und finden Sie den passenden Termin beim Bürgeramt.</p>
                <Link to={"dashboard"} >
                    <button className="px-8 py-4 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transform hover:scale-105 transition duration-500 shadow-lg">
                        Jetzt Termin suchen
                    </button>

                </Link>
            </section>

            {/* Footer */}
            <footer className="px-6 md:px-20 py-10 text-center bg-gray-200 dark:bg-gray-900 text-gray-700 dark:text-gray-300">
                &copy; 2025 Bürgeramt Slot Finder. Alle Rechte vorbehalten.
            </footer>

            {/* Animations */}
            <style>
                {`@keyframes fadeInLeft { from {opacity:0; transform: translateX(-50px);} to {opacity:1; transform: translateX(0);} }
        @keyframes fadeInRight { from {opacity:0; transform: translateX(50px);} to {opacity:1; transform: translateX(0);} }
        @keyframes fadeInUp { from {opacity:0; transform: translateY(20px);} to {opacity:1; transform: translateY(0);} }
        .animate-fadeInLeft { animation: fadeInLeft 1s ease forwards; }
        .animate-fadeInRight { animation: fadeInRight 1s ease forwards; }
        .animate-fadeInUp { animation: fadeInUp 1s ease forwards; }
        .animate-fadeIn { animation: fadeInUp 1s 0.5s ease forwards; opacity:0; }
        `}
            </style>
        </div>
    );
};

export default LandingPage;
