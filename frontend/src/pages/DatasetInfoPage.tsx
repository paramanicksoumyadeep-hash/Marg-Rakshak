import { Database, ExternalLink, ShieldCheck } from 'lucide-react';

const datasets = [
  {
    title: 'Triple Bike Riding Detection',
    description: 'Roboflow Universe dataset trained specifically for detecting triple pillion riding violations on two-wheelers.',
    link: 'https://universe.roboflow.com/suseendrakumars-workspace/triple-riding-model',
    image: '/datasets/triple.jpg',
    tags: ['Roboflow', 'YOLOv8', 'Object Detection']
  },
  {
    title: 'Red Light Violation Detection',
    description: 'Specialized dataset for tracking vehicle trajectory across red light demarcations at signalized intersections.',
    link: 'https://universe.roboflow.com/traffic-violation-detected/red-light-violation-detect-dataset/dataset/3',
    image: '/datasets/redlight.jpg',
    tags: ['Roboflow', 'Trajectory', 'Signal Sync']
  },
  {
    title: 'Illegal Parking Detection',
    description: 'Annotated bounding boxes for vehicles parked in restricted zones, bus stops, and no-parking areas.',
    link: 'https://universe.roboflow.com/thesis-gsgcj/illegal-parking-qrvua/dataset/1',
    image: '/datasets/parking.jpg',
    tags: ['Roboflow', 'Spatial Analysis']
  },
  {
    title: 'Wrong Way Driving Detection',
    description: 'Directional vector-based dataset for identifying vehicles moving against the designated traffic flow.',
    link: 'https://universe.roboflow.com/trafficlightupdation/wrong-way-driving-detection-htaqa/dataset/1',
    image: '/datasets/wrongway.jpg',
    tags: ['Roboflow', 'Vector Math']
  },
  {
    title: 'Indian Driving Dataset (IDD)',
    description: 'The premier benchmark for unstructured traffic environments. Used for robust vehicle identification and segmentation in Indian conditions.',
    link: 'https://idd.insaan.iiit.ac.in/',
    image: '/datasets/idd.jpg',
    tags: ['IIIT Hyderabad', 'Segmentation', 'Benchmark']
  },
  {
    title: 'CCTV Surveillance Topography',
    description: 'Official State/UTs wise availability of CCTV cameras dataset sourced directly from Open Government Data Platform India.',
    link: 'https://www.data.gov.in/resource/stateuts-wise-availability-cctv-camera-under-availability-grievance-redressel-mechanism',
    image: '/datasets/cctv.jpg',
    tags: ['Data.gov.in', 'Geospatial', 'Open Data']
  }
];

const DatasetInfoPage = () => {
  return (
    <div className="max-w-7xl mx-auto mt-6 pb-16">
      <div className="mb-10 flex items-center gap-4">
        <div className="bg-[#C8102E]/10 p-3 rounded-2xl">
          <Database className="w-10 h-10 text-[#C8102E]" />
        </div>
        <div>
          <h2 className="text-4xl font-black text-gray-900 dark:text-white tracking-tight">Dataset Architecture</h2>
          <p className="text-gray-500 dark:text-gray-400 mt-2 text-lg font-medium">Over 56,000+ specialized images & authoritative geospatial feeds powering Marg Rakshak.</p>
        </div>
      </div>

      <div className="bg-yellow-50 dark:bg-yellow-900/10 border border-yellow-200 dark:border-yellow-900/50 p-6 rounded-2xl mb-12 flex items-start gap-4">
        <ShieldCheck className="text-yellow-600 dark:text-yellow-500 shrink-0 mt-1" size={24} />
        <div>
          <h3 className="font-bold text-gray-900 dark:text-white text-lg">Zero Fake Data Policy</h3>
          <p className="text-gray-600 dark:text-gray-400 mt-1">
            Every model in the Marg Rakshak ecosystem has been trained on real, specialized datasets. We do not use mock inferences. The links below trace directly to the authentic sources used to fine-tune our YOLOv8 architecture for Indian topography.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {datasets.map((dataset, idx) => (
          <a 
            key={idx} 
            href={dataset.link} 
            target="_blank" 
            rel="noopener noreferrer"
            className="group flex flex-col bg-white dark:bg-gray-800 rounded-3xl overflow-hidden shadow-sm hover:shadow-xl border border-gray-200 dark:border-gray-700 transition-all duration-300 hover:-translate-y-1"
          >
            {/* Cardboard Image Header */}
            <div className="h-48 w-full overflow-hidden relative">
              <div className="absolute inset-0 bg-gray-900/20 group-hover:bg-transparent transition-colors duration-300 z-10" />
              <img 
                src={dataset.image} 
                alt={dataset.title} 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div className="absolute top-4 right-4 z-20 bg-white/90 dark:bg-gray-900/90 backdrop-blur-md p-2 rounded-full shadow-lg opacity-0 group-hover:opacity-100 transition-opacity">
                <ExternalLink size={18} className="text-[#C8102E] dark:text-red-500" />
              </div>
            </div>

            {/* Content Body */}
            <div className="p-6 flex flex-col flex-1">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3 group-hover:text-[#C8102E] dark:group-hover:text-red-500 transition-colors">
                {dataset.title}
              </h3>
              
              <p className="text-gray-600 dark:text-gray-400 text-sm flex-1 leading-relaxed mb-6">
                {dataset.description}
              </p>

              {/* Tags */}
              <div className="flex flex-wrap gap-2 mt-auto">
                {dataset.tags.map(tag => (
                  <span key={tag} className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 rounded-full text-xs font-semibold">
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
};

export default DatasetInfoPage;
