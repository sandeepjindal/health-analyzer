import React, { useState } from 'react';
import axios from 'axios';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  AreaChart, Area
} from 'recharts';
import './App.css';

const API_BASE = 'http://localhost:5000/api';
const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe'];

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [insights, setInsights] = useState(null);
  const [activeTab, setActiveTab] = useState('overview');

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setData(response.data.data);
      setInsights(response.data.insights);
      setActiveTab('overview');
    } catch (error) {
      alert('Error uploading file: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>💓 Garmin Health Analyzer</h1>
        <p>Understand your stress, HRV, and heart rate patterns</p>
      </header>

      <main className="container">
        {/* Upload Section */}
        <section className="upload-section">
          <h2>📤 Upload Your Garmin Data</h2>
          <div className="upload-box">
            <input
              type="file"
              onChange={handleFileChange}
              accept=".tcx,.csv,.fit"
              disabled={loading}
            />
            <button
              onClick={handleUpload}
              disabled={loading || !selectedFile}
              className="btn-primary"
            >
              {loading ? 'Processing...' : 'Upload & Analyze'}
            </button>
          </div>
          <p className="file-hint">Supported formats: TCX, CSV, FIT</p>
        </section>

        {/* Results Section */}
        {data && insights && (
          <>
            <section className="tabs">
              <button
                className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
                onClick={() => setActiveTab('overview')}
              >
                Overview
              </button>
              <button
                className={`tab ${activeTab === 'stress' ? 'active' : ''}`}
                onClick={() => setActiveTab('stress')}
              >
                Stress Analysis
              </button>
              <button
                className={`tab ${activeTab === 'hrv' ? 'active' : ''}`}
                onClick={() => setActiveTab('hrv')}
              >
                HRV Analysis
              </button>
              <button
                className={`tab ${activeTab === 'hr' ? 'active' : ''}`}
                onClick={() => setActiveTab('hr')}
              >
                Heart Rate
              </button>
              <button
                className={`tab ${activeTab === 'activities' ? 'active' : ''}`}
                onClick={() => setActiveTab('activities')}
              >
                Activities
              </button>
            </section>

            {/* Overview Tab */}
            {activeTab === 'overview' && (
              <section className="overview">
                <div className="stats-grid">
                  <div className="stat-card">
                    <h3>Average HR</h3>
                    <p className="stat-value">{insights.hr_patterns.avg_hr.toFixed(0)} bpm</p>
                  </div>
                  <div className="stat-card">
                    <h3>Avg Stress</h3>
                    <p className="stat-value">{insights.stress_analysis.avg_stress.toFixed(0)}</p>
                  </div>
                  <div className="stat-card">
                    <h3>Avg HRV</h3>
                    <p className="stat-value">{insights.hrv_analysis.avg_hrv.toFixed(0)} ms</p>
                  </div>
                  <div className="stat-card">
                    <h3>Activities</h3>
                    <p className="stat-value">{insights.activity_summary.total_activities}</p>
                  </div>
                </div>

                <div className="recommendations">
                  <h3>💡 Recommendations</h3>
                  <div className="rec-list">
                    {[
                      ...(insights.stress_analysis.recommendations || []),
                      ...(insights.hrv_analysis.recommendations || [])
                    ].map((rec, idx) => (
                      <div key={idx} className="rec-item">✓ {rec}</div>
                    ))}
                  </div>
                </div>
              </section>
            )}

            {/* Stress Tab */}
            {activeTab === 'stress' && (
              <section className="stress-section">
                <h2>📊 Stress Analysis</h2>
                <div className="metrics">
                  <div className="metric">
                    <span>Avg Stress:</span>
                    <strong>{insights.stress_analysis.avg_stress.toFixed(0)}</strong>
                  </div>
                  <div className="metric">
                    <span>Max Stress:</span>
                    <strong>{insights.stress_analysis.max_stress}</strong>
                  </div>
                  <div className="metric">
                    <span>Min Stress:</span>
                    <strong>{insights.stress_analysis.min_stress}</strong>
                  </div>
                  <div className="metric">
                    <span>High Stress %:</span>
                    <strong>{insights.stress_analysis.high_stress_count}/{data.stress_data.length}</strong>
                  </div>
                </div>

                {/* Stress Distribution Chart */}
                {data.stress_data && data.stress_data.length > 0 && (
                  <div className="chart-container">
                    <h3>Stress Levels Throughout Day</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <AreaChart data={data.stress_data.map(d => ({
                        time: new Date(d.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
                        stress: d.stress_level
                      }))}>
                        <defs>
                          <linearGradient id="stressGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#ff6b6b" stopOpacity={0.8}/>
                            <stop offset="95%" stopColor="#ff6b6b" stopOpacity={0.1}/>
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="time" angle={-45} height={80} />
                        <YAxis />
                        <Tooltip />
                        <Area
                          type="monotone"
                          dataKey="stress"
                          stroke="#ff6b6b"
                          fillOpacity={1}
                          fill="url(#stressGrad)"
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                )}

                <h3>High Stress Periods</h3>
                {insights.stress_analysis.high_stress_periods?.length > 0 ? (
                  <div className="periods-list">
                    {insights.stress_analysis.high_stress_periods.map((period, idx) => (
                      <div key={idx} className="period-item">
                        <p>
                          <strong>{new Date(period.start).toLocaleTimeString()}</strong> - Peak: {period.peak} | Avg: {period.avg.toFixed(0)} | Duration: {period.duration_minutes} min
                        </p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p>No high stress periods detected</p>
                )}

                <div className="recommendations">
                  <h3>💡 Recommendations</h3>
                  <div className="rec-list">
                    {(insights.stress_analysis.recommendations || []).map((rec, idx) => (
                      <div key={idx} className="rec-item">✓ {rec}</div>
                    ))}
                  </div>
                </div>
              </section>
            )}

            {/* HRV Tab */}
            {activeTab === 'hrv' && (
              <section className="hrv-section">
                <h2>❤️ HRV Analysis</h2>
                <div className="metrics">
                  <div className="metric">
                    <span>Avg HRV:</span>
                    <strong>{insights.hrv_analysis.avg_hrv.toFixed(0)} ms</strong>
                  </div>
                  <div className="metric">
                    <span>Max HRV:</span>
                    <strong>{insights.hrv_analysis.max_hrv.toFixed(0)} ms</strong>
                  </div>
                  <div className="metric">
                    <span>Std Dev:</span>
                    <strong>{insights.hrv_analysis.std_dev.toFixed(0)}</strong>
                  </div>
                  <div className="metric">
                    <span>Category:</span>
                    <strong className={`category-${insights.hrv_analysis.hrv_category.toLowerCase()}`}>
                      {insights.hrv_analysis.hrv_category}
                    </strong>
                  </div>
                </div>

                <div className="metrics">
                  <div className="metric">
                    <span>Recovery Status:</span>
                    <strong className={`recovery-${insights.hrv_analysis.recovery_status.toLowerCase()}`}>
                      {insights.hrv_analysis.recovery_status}
                    </strong>
                  </div>
                  <div className="metric">
                    <span>Trend:</span>
                    <strong>{insights.hrv_analysis.trend}</strong>
                  </div>
                  <div className="metric">
                    <span>Trend Slope:</span>
                    <strong>{insights.hrv_analysis.trend_slope.toFixed(2)}</strong>
                  </div>
                </div>

                {/* HRV Distribution Chart */}
                {data.hrv_data && data.hrv_data.length > 0 && (
                  <div className="chart-container">
                    <h3>HRV Trend Over Time</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={data.hrv_data.map((d, i) => ({
                        index: i,
                        hrv: d.hrv_value,
                        time: new Date(d.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})
                      }))}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="time" angle={-45} height={80} />
                        <YAxis />
                        <Tooltip />
                        <Line
                          type="monotone"
                          dataKey="hrv"
                          stroke="#667eea"
                          strokeWidth={2}
                          dot={false}
                          isAnimationActive={true}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                )}

                <div className="recommendations">
                  <h3>💡 Recommendations</h3>
                  <div className="rec-list">
                    {(insights.hrv_analysis.recommendations || []).map((rec, idx) => (
                      <div key={idx} className="rec-item">✓ {rec}</div>
                    ))}
                  </div>
                </div>
              </section>
            )}

            {/* HR Tab */}
            {activeTab === 'hr' && (
              <section className="hr-section">
                <h2>💗 Heart Rate Patterns</h2>
                <div className="metrics">
                  <div className="metric">
                    <span>Avg HR:</span>
                    <strong>{insights.hr_patterns.avg_hr.toFixed(0)} bpm</strong>
                  </div>
                  <div className="metric">
                    <span>Resting HR:</span>
                    <strong>{insights.hr_patterns.resting_hr} bpm</strong>
                  </div>
                  <div className="metric">
                    <span>Max HR:</span>
                    <strong>{insights.hr_patterns.max_hr} bpm</strong>
                  </div>
                  <div className="metric">
                    <span>Min HR:</span>
                    <strong>{insights.hr_patterns.min_hr} bpm</strong>
                  </div>
                </div>

                {/* HR Trend Chart */}
                {data.heart_rate_data && data.heart_rate_data.length > 0 && (
                  <div className="chart-container">
                    <h3>Heart Rate Throughout Day</h3>
                    <ResponsiveContainer width="100%" height={300}>
                      <AreaChart data={data.heart_rate_data.map(d => ({
                        time: new Date(d.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
                        hr: d.bpm
                      }))}>
                        <defs>
                          <linearGradient id="hrGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#667eea" stopOpacity={0.8}/>
                            <stop offset="95%" stopColor="#667eea" stopOpacity={0.1}/>
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="time" angle={-45} height={80} />
                        <YAxis />
                        <Tooltip />
                        <Area
                          type="monotone"
                          dataKey="hr"
                          stroke="#667eea"
                          fillOpacity={1}
                          fill="url(#hrGrad)"
                        />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                )}

                <h3>HR Zones Distribution</h3>
                {insights.hr_patterns.zone_distribution && (
                  <>
                    {/* Zone Pie Chart */}
                    <div className="chart-container">
                      <ResponsiveContainer width="100%" height={300}>
                        <PieChart>
                          <Pie
                            data={Object.entries(insights.hr_patterns.zone_distribution).map(([name, value]) => ({
                              name: name.replace(/_/g, ' '),
                              value: value
                            }))}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            label={({ name, value }) => `${name}: ${value}`}
                            outerRadius={80}
                            fill="#8884d8"
                            dataKey="value"
                          >
                            {Object.entries(insights.hr_patterns.zone_distribution).map((_, index) => (
                              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                            ))}
                          </Pie>
                          <Tooltip />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>

                    {/* Zone Details */}
                    <div className="zones">
                      {Object.entries(insights.hr_patterns.zone_distribution || {}).map(([zone, count], idx) => {
                        const zoneInfo = {
                          'zone1_recovery': { name: 'Zone 1: Recovery', color: '#4caf50', range: 'Easy' },
                          'zone2_base': { name: 'Zone 2: Base', color: '#8bc34a', range: 'Steady' },
                          'zone3_build': { name: 'Zone 3: Build', color: '#ffc107', range: 'Tempo' },
                          'zone4_hard': { name: 'Zone 4: Hard', color: '#ff9800', range: 'Threshold' },
                          'zone5_max': { name: 'Zone 5: Max', color: '#f44336', range: 'VO2 Max' }
                        };
                        const info = zoneInfo[zone];
                        return (
                          <div key={zone} className="zone-item" style={{ borderLeftColor: info.color }}>
                            <div className="zone-header">
                              <span className="zone-name">{info.name}</span>
                              <span className="zone-range">{info.range}</span>
                            </div>
                            <div className="zone-bar" style={{backgroundColor: info.color, width: `${(count / 100) * 100}%`}}></div>
                            <span className="zone-count">{count} readings</span>
                          </div>
                        );
                      })}
                    </div>
                  </>
                )}
              </section>
            )}

            {/* Activities Tab */}
            {activeTab === 'activities' && (
              <section className="activities-section">
                <h2>🏃 Activities</h2>
                <div className="metrics">
                  <div className="metric">
                    <span>Total Activities:</span>
                    <strong>{insights.activity_summary.total_activities}</strong>
                  </div>
                  <div className="metric">
                    <span>Total Duration:</span>
                    <strong>{insights.activity_summary.total_duration_minutes} min</strong>
                  </div>
                  <div className="metric">
                    <span>Total Calories:</span>
                    <strong>{insights.activity_summary.total_calories}</strong>
                  </div>
                </div>

                <h3>Activity List</h3>
                {insights.activity_summary.activities?.length > 0 ? (
                  <div className="activities-list">
                    {insights.activity_summary.activities.map((activity, idx) => (
                      <div key={idx} className="activity-item">
                        <p>
                          <strong>{activity.name}</strong> | {activity.duration_minutes} min | {activity.calories} cal | HR: {activity.avg_hr} - {activity.max_hr} bpm
                        </p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p>No activities found</p>
                )}
              </section>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
