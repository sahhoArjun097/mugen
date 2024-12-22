import React from "react";
import { Link } from "react-router-dom";

const DashboardPage = () => {
  return (
    <div className="homeBackgroundImage min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white">
      <h1 className="sm:text-6xl md:text-6xl lg:text-7xl text-5xl font-bold mb-6">Welcome to MuGen AI</h1>
      <p className="text-lg mb-8">Manage your music, generate tracks, and explore features.</p>
      <div className="flex space-x-4">
        <Link
          to="/generate"
          className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-all"
        >
          Generate Music
        </Link>
        <Link
          to="/mymusic"
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all"
        >
          My Music
        </Link>
      </div>
    </div>
  );
};





export default DashboardPage;