import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Shield, Sun, Moon, Menu, X, LogOut } from 'lucide-react';
import LandingPage from './pages/LandingPage';
import SurveillanceMapPage from './pages/SurveillanceMapPage';
import GenerateChallanPage from './pages/GenerateChallanPage';
import ResultsPage from './pages/ResultsPage';
import DossierPage from './pages/DossierPage';
import AnalyticsPage from './pages/AnalyticsPage';
import DatasetInfoPage from './pages/DatasetInfoPage';
import AuthPage from './pages/AuthPage';
import { AuthProvider, useAuth } from './context/AuthContext';

const TopNavbar = ({ isDark, setIsDark }: { isDark: boolean, setIsDark: (val: boolean) => void }) => {
  const location = useLocation();
  const { logout, name, isSurveyor } = useAuth();
  const [menuOpen, setMenuOpen] = useState(false);

  const links = [
    { path: '/', label: 'Overview' },
    { path: '/map', label: 'Cameras' },
    { path: '/generate-challan', label: 'Generate Challan' },
    { path: '/analytics', label: 'Analytics' },
    { path: '/datasets', label: 'Datasets' },
  ];

  return (
    <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 sticky top-0 z-50 transition-colors duration-300">
      <div className="max-w-[1400px] mx-auto px-4 sm:px-6 h-16 sm:h-20 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-2 sm:gap-4 border-r border-transparent sm:border-gray-300 dark:sm:border-gray-700 pr-0 sm:pr-6 mr-0 sm:mr-2">
          <Shield className="text-[#C8102E] dark:text-red-500" size={24} />
          <h1 className="font-bold text-lg sm:text-xl tracking-tight text-gray-900 dark:text-white sm:block hidden">Marg Rakshak</h1>
        </div>

        {/* Mobile Menu Toggle */}
        <button 
          className="sm:hidden p-2 text-gray-600 dark:text-gray-300"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          {menuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>

        {/* Navigation Links - Desktop */}
        <nav className="hidden sm:flex flex-1 items-center gap-4 lg:gap-8 px-4">
          {links.map(l => {
            const isActive = location.pathname === l.path || (l.path !== '/' && location.pathname.startsWith(l.path));
            return (
              <Link
                key={l.path}
                to={l.path}
                className={`font-semibold text-sm lg:text-[15px] transition-colors relative h-20 flex items-center ${
                  isActive 
                    ? 'text-gray-900 dark:text-white' 
                    : 'text-gray-500 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                }`}
              >
                {l.label}
                {isActive && (
                  <span className="absolute bottom-0 left-0 w-full h-1 bg-[#C8102E] dark:bg-red-500 rounded-t-full" />
                )}
              </Link>
            );
          })}
        </nav>

        {/* Right Actions - Desktop */}
        <div className="hidden sm:flex items-center gap-4 lg:gap-6">
          <div className="text-sm font-medium text-gray-600 dark:text-gray-300 max-w-[150px] truncate">
            {name} {isSurveyor && <span className="text-xs opacity-70">(Demo)</span>}
          </div>
          <button 
            onClick={logout}
            title="Log Out"
            className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-300 transition-colors"
          >
            <LogOut size={20} />
          </button>
          <button 
            onClick={() => setIsDark(!isDark)}
            className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-300 transition-colors"
          >
            {isDark ? <Sun size={20} /> : <Moon size={20} />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="sm:hidden border-t border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 absolute top-[100%] w-full left-0 p-4 shadow-lg flex flex-col gap-4 max-h-[calc(100vh-64px)] overflow-y-auto">
          <nav className="flex flex-col gap-2">
            {links.map(l => {
              const isActive = location.pathname === l.path || (l.path !== '/' && location.pathname.startsWith(l.path));
              return (
                <Link
                  key={l.path}
                  to={l.path}
                  onClick={() => setMenuOpen(false)}
                  className={`p-3 rounded-lg font-semibold text-[15px] transition-colors ${
                    isActive 
                      ? 'bg-red-50 dark:bg-red-900/20 text-[#C8102E] dark:text-red-500' 
                      : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'
                  }`}
                >
                  {l.label}
                </Link>
              );
            })}
          </nav>
          <div className="flex items-center justify-between border-t border-gray-200 dark:border-gray-800 pt-4 mt-2">
            <div className="text-sm font-medium text-gray-600 dark:text-gray-300 truncate pr-4">
              {name} {isSurveyor && '(Demo)'}
            </div>
            <div className="flex gap-2 shrink-0">
              <button onClick={() => setIsDark(!isDark)} className="p-2 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300">
                {isDark ? <Sun size={20} /> : <Moon size={20} />}
              </button>
              <button onClick={logout} className="p-2 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300">
                <LogOut size={20} />
              </button>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

function MainApp({ isDark, setIsDark }: { isDark: boolean, setIsDark: (val: boolean) => void }) {
  const { name, isSurveyor } = useAuth();

  if (!name && !isSurveyor) {
    return <AuthPage />;
  }

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors duration-300 flex flex-col w-full overflow-x-hidden">
      <TopNavbar isDark={isDark} setIsDark={setIsDark} />
      <main className="flex-1 w-full max-w-[1400px] mx-auto p-4 sm:p-8">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/map" element={<SurveillanceMapPage />} />
          <Route path="/generate-challan" element={<GenerateChallanPage />} />
          <Route path="/results/:batchId" element={<ResultsPage />} />
          <Route path="/plates/:number" element={<DossierPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/datasets" element={<DatasetInfoPage />} />
        </Routes>
      </main>
      
      {/* Global Footer */}
      <footer className="bg-black dark:bg-white py-12 sm:py-16 mt-auto transition-colors duration-300 w-full">
        <div className="max-w-[1400px] mx-auto px-4 sm:px-8 flex flex-col md:flex-row items-center justify-between text-sm text-gray-400 dark:text-gray-600">
          <div className="flex items-center justify-center md:justify-start gap-2 mb-4 md:mb-0">
            <Shield size={18} className="text-[#C8102E] dark:text-red-600" />
            <span className="font-bold text-white dark:text-black text-base tracking-wide">Marg Rakshak</span>
            <span className="mx-2 opacity-30 hidden sm:inline">|</span>
            <span className="hidden sm:inline">&copy; {new Date().getFullYear()}</span>
          </div>
          <div className="text-center md:text-right font-medium">
            Command Intelligence Platform
            <div className="text-xs mt-1 text-gray-500 dark:text-gray-500 uppercase tracking-widest">
              Bengaluru Traffic Police
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

function App() {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [isDark]);

  return (
    <AuthProvider>
      <BrowserRouter>
        <MainApp isDark={isDark} setIsDark={setIsDark} />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
