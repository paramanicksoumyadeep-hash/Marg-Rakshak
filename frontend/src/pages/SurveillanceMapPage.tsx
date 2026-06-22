import { useState, useEffect, useMemo } from 'react';
import { MapPin, Camera, AlertTriangle } from 'lucide-react';
import { MapContainer, TileLayer, Marker, Tooltip } from 'react-leaflet';
import L from 'leaflet';

const SurveillanceMapPage = () => {
  const [cameras, setCameras] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedNode, setSelectedNode] = useState<any | null>(null);
  const [activeFilter, setActiveFilter] = useState<'all' | 'cctv' | 'hotspot'>('all');

  // Custom DivIcon for the camera emoji
  const createEmojiIcon = (emoji: string, size: number) => new L.DivIcon({
    html: `<div style="font-size: ${size}px; line-height: 1; text-align: center; filter: drop-shadow(0px 2px 4px rgba(0,0,0,0.3));">${emoji}</div>`,
    className: 'bg-transparent border-0',
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
    popupAnchor: [0, -size / 2],
  });

  useEffect(() => {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const url = searchQuery.trim() 
      ? `${apiUrl}/api/cameras?q=${encodeURIComponent(searchQuery)}`
      : `${apiUrl}/api/cameras`;
      
    fetch(url)
      .then(res => res.json())
      .then(data => setCameras(data?.cameras || []))
      .catch(err => console.error("Failed to fetch cameras:", err));
  }, [searchQuery]);

  const displayedCameras = useMemo(() => {
    if (activeFilter === 'cctv') return cameras.filter(c => c.type === 'active');
    if (activeFilter === 'hotspot') return cameras.filter(c => c.type === 'hotspot');
    return cameras;
  }, [cameras, activeFilter]);

  return (
    <div className="w-full max-w-[1400px] mx-auto px-4 h-[calc(100vh-120px)] bg-white dark:bg-gray-900 transition-colors duration-300">
      
      <div className="flex flex-col lg:flex-row gap-6 h-full">
        
        {/* Map Container - Left Side */}
        <div className="flex-1 relative rounded-2xl overflow-hidden shadow-lg border border-gray-200 dark:border-gray-800 bg-gray-100 dark:bg-gray-800 flex flex-col">
          
          {/* Bottom Control Bar Overlay */}
          <div className="absolute bottom-6 left-0 right-0 z-[1000] flex flex-col items-center gap-3 px-4 pointer-events-none">
            
            {/* Search Bar */}
            <form 
              onSubmit={(e) => e.preventDefault()}
              className="w-full max-w-md relative group flex items-center bg-white/95 dark:bg-gray-900/95 backdrop-blur-md rounded-full shadow-lg border border-gray-200 dark:border-gray-700 overflow-hidden pointer-events-auto"
            >
              <input 
                type="text" 
                placeholder="Search area (e.g. Koramangala)" 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1 pl-6 pr-4 py-3 bg-transparent text-gray-900 dark:text-white text-sm font-medium focus:outline-none placeholder-gray-500 dark:placeholder-gray-400"
              />
              <button 
                type="submit"
                className="bg-[#C8102E] hover:bg-[#A00D24] text-white px-6 py-2 rounded-full m-1 font-bold text-sm transition-colors shadow-sm"
              >
                Find
              </button>
            </form>

          </div>

          <MapContainer 
            center={[12.9716, 77.5946]} 
            zoom={12} 
            scrollWheelZoom={true} 
            className="w-full flex-1 z-0"
            zoomControl={true}
          >
            <TileLayer
              url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"
              attribution='&copy; Google Maps'
            />
            {displayedCameras.map(cam => {
              const isHotspot = cam.type === 'hotspot';
              const emoji = isHotspot ? '📍' : '📹';
              const severityVal = typeof cam.severity === 'number' ? cam.severity : 50;
              const iconSize = isHotspot ? 24 : Math.max(16, Math.min(28, severityVal / 3));

              return (
                <Marker 
                  key={cam.id} 
                  position={[cam.lat || 12.9716, cam.lng || 77.5946]}
                  icon={createEmojiIcon(emoji, iconSize)}
                  eventHandlers={{
                    click: () => setSelectedNode(cam),
                  }}
                >
                  <Tooltip 
                    direction="top" 
                    offset={[0, -(iconSize / 2)]} 
                    className="font-bold text-xs bg-gray-900 text-white border-0 shadow-lg px-2 py-1 rounded-md"
                  >
                    {cam.name}
                  </Tooltip>
                </Marker>
              );
            })}
          </MapContainer>
        </div>

        {/* Right Sidebar - Analytics Panel */}
        <div className="w-full lg:w-96 flex flex-col gap-4">
          
          {/* Top Panel: Toggles */}
          <div className="flex gap-2">
            <button 
              onClick={() => setActiveFilter(activeFilter === 'cctv' ? 'all' : 'cctv')}
              className={`flex-1 flex flex-col items-center justify-center p-3 rounded-xl border transition-colors ${
                activeFilter === 'cctv' 
                  ? 'bg-green-50 border-green-200 text-green-700 dark:bg-green-900/30 dark:border-green-800 dark:text-green-400' 
                  : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700'
              }`}
            >
              <Camera size={20} className="mb-1" />
              <span className="text-sm font-bold">Locate CCTV</span>
            </button>
            <button 
              onClick={() => setActiveFilter(activeFilter === 'hotspot' ? 'all' : 'hotspot')}
              className={`flex-1 flex flex-col items-center justify-center p-3 rounded-xl border transition-colors ${
                activeFilter === 'hotspot' 
                  ? 'bg-orange-50 border-orange-200 text-orange-700 dark:bg-orange-900/30 dark:border-orange-800 dark:text-orange-400' 
                  : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700'
              }`}
            >
              <AlertTriangle size={20} className="mb-1" />
              <span className="text-sm font-bold text-center leading-tight">Unmonitored Hotspots</span>
            </button>
          </div>

          {/* Bottom Panel: Selected Node Details */}
          <div className="flex-1 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 flex flex-col overflow-y-auto">
            {selectedNode ? (
              <div className="flex flex-col h-full">
                <h2 className="text-2xl font-black text-gray-900 dark:text-white mb-3 leading-tight">{selectedNode.name}</h2>
                
                <div className="mb-8">
                  <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold ${
                    selectedNode.type === 'active' 
                      ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' 
                      : 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400'
                  }`}>
                    {selectedNode.type === 'active' ? 'Active Camera Node' : 'Unmonitored Hotspot'}
                  </span>
                </div>
                
                <div className="flex flex-col gap-4">
                  <div className="border border-gray-200 dark:border-gray-700 rounded-xl p-5">
                    <p className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">Severity Index</p>
                    <p className="text-4xl font-black text-gray-900 dark:text-white">{selectedNode.severity || 'N/A'}</p>
                  </div>
                  
                  <div className="border border-gray-200 dark:border-gray-700 rounded-xl p-5">
                    <p className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2">Recorded Violations</p>
                    <p className="text-4xl font-black text-[#C8102E] dark:text-red-500">{(selectedNode.violations || 0).toLocaleString()}</p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-center px-4 opacity-60">
                <MapPin size={48} className="text-gray-300 dark:text-gray-600 mb-4" />
                <p className="text-gray-500 font-medium">Select any camera node or hotspot on the map to view detailed analytics.</p>
              </div>
            )}
          </div>
          
        </div>
      </div>
    </div>
  );
};

export default SurveillanceMapPage;
