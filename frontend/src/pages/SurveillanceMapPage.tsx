import { useState, useEffect, useMemo } from 'react';
import { MapPin, Camera, AlertTriangle } from 'lucide-react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';

const SurveillanceMapPage = () => {
  const [cameras, setCameras] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedNode, setSelectedNode] = useState<any | null>(null);
  const [activeFilter] = useState<'all' | 'cctv' | 'hotspot'>('all');

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
    <div className="max-w-[1400px] mx-auto h-[calc(100vh-120px)] bg-white dark:bg-gray-900 transition-colors duration-300">
      
      <div className="flex flex-col lg:flex-row gap-6 h-full">
        
        {/* Map Container - Left Side */}
        <div className="flex-1 relative rounded-2xl overflow-hidden shadow-lg border border-gray-200 dark:border-gray-800 bg-gray-100 dark:bg-gray-800 flex flex-col">
          
          {/* Top Control Bar Overlay */}
          <div className="absolute top-6 left-0 right-0 z-[1000] flex flex-col items-center gap-3 px-4 pointer-events-none">
            
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
                  <Popup className="rounded-xl overflow-hidden shadow-xl border-0">
                    <div className="p-3 bg-white dark:bg-gray-800 text-gray-900 dark:text-white min-w-[200px]">
                      <h4 className="font-bold text-lg mb-1">{cam.name}</h4>
                      <div className="flex items-center gap-2 text-sm text-gray-500 dark:text-gray-400 mb-3">
                        <MapPin size={14} />
                        <span>{cam.type === 'active' ? 'Active CCTV Node' : 'Violation Hotspot'}</span>
                      </div>
                      
                      <div className="grid grid-cols-2 gap-2 mt-4 pt-3 border-t border-gray-100 dark:border-gray-700">
                        <div>
                          <p className="text-xs text-gray-400 dark:text-gray-500 font-medium">Status</p>
                          <p className="font-bold text-green-600 dark:text-green-400 text-sm">{cam.type === 'active' ? 'Online' : 'Warning'}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-400 dark:text-gray-500 font-medium">Violations</p>
                          <p className="font-bold text-[#C8102E] dark:text-red-500 text-sm">{(cam.violations || 0).toLocaleString()}</p>
                        </div>
                      </div>
                    </div>
                  </Popup>
                </Marker>
              );
            })}
          </MapContainer>
        </div>

        {/* Right Sidebar - Analytics Panel */}
        <div className="w-full lg:w-96 flex flex-col gap-6">
          
          {/* Top Panel: System Status */}
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-lg font-black text-gray-900 dark:text-white mb-4">Network Status</h3>
            <div className="space-y-4">
              <div className="flex justify-between items-center bg-gray-50 dark:bg-gray-900 p-4 rounded-xl border border-gray-100 dark:border-gray-700">
                <div className="flex items-center gap-3">
                  <div className="bg-green-100 dark:bg-green-900/30 p-2 rounded-lg">
                    <Camera className="text-green-600 dark:text-green-400" size={20} />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-gray-900 dark:text-white">Active Feeds</p>
                    <p className="text-xs text-gray-500 font-medium">Online</p>
                  </div>
                </div>
                <span className="text-2xl font-black text-gray-900 dark:text-white">200</span>
              </div>
              
              <div className="flex justify-between items-center bg-gray-50 dark:bg-gray-900 p-4 rounded-xl border border-gray-100 dark:border-gray-700">
                <div className="flex items-center gap-3">
                  <div className="bg-red-100 dark:bg-red-900/30 p-2 rounded-lg">
                    <AlertTriangle className="text-red-600 dark:text-red-400" size={20} />
                  </div>
                  <div>
                    <p className="text-sm font-bold text-gray-900 dark:text-white">Hotspots</p>
                    <p className="text-xs text-gray-500 font-medium">High Severity</p>
                  </div>
                </div>
                <span className="text-2xl font-black text-gray-900 dark:text-white">200</span>
              </div>
            </div>
          </div>

          {/* Bottom Panel: Selected Node Details */}
          <div className="flex-1 bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 flex flex-col">
            <h3 className="text-lg font-black text-gray-900 dark:text-white mb-4">Node Intelligence</h3>
            
            {selectedNode ? (
              <div className="flex-1 flex flex-col">
                <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-xl border border-gray-100 dark:border-gray-700 mb-4">
                  <h4 className="font-bold text-gray-900 dark:text-white text-lg">{selectedNode.name}</h4>
                  <p className="text-sm text-gray-500 mt-1 capitalize">{selectedNode.type} Node</p>
                </div>
                
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-xl border border-gray-100 dark:border-gray-700">
                    <p className="text-xs text-gray-500 font-medium mb-1">Total Infractions</p>
                    <p className="text-xl font-black text-[#C8102E] dark:text-red-500">{(selectedNode.violations || 0).toLocaleString()}</p>
                  </div>
                  <div className="bg-gray-50 dark:bg-gray-900 p-4 rounded-xl border border-gray-100 dark:border-gray-700">
                    <p className="text-xs text-gray-500 font-medium mb-1">Uptime</p>
                    <p className="text-xl font-black text-green-600 dark:text-green-400">99.9%</p>
                  </div>
                </div>

                <div className="mt-auto">
                  <button className="w-full bg-gray-900 dark:bg-white text-white dark:text-gray-900 font-bold py-3 px-4 rounded-xl hover:bg-gray-800 dark:hover:bg-gray-100 transition-colors shadow-sm">
                    View Live Feed
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-center px-4 opacity-60">
                <MapPin size={48} className="text-gray-300 dark:text-gray-600 mb-4" />
                <p className="text-gray-500 font-medium">Select any camera node or hotspot on the map to view detailed analytics and live feeds.</p>
              </div>
            )}
          </div>
          
        </div>
      </div>
    </div>
  );
};

export default SurveillanceMapPage;
