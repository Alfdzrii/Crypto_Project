/**
 * Dashboard Main JavaScript
 * Handles real-time updates, AJAX polling, and user interactions
 */

// Configuration
const POLL_INTERVAL = 2000; // 2 seconds
let pollingTimer = null;
let isPolling = false;

// DOM Elements
let elements = {};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 IDS Dashboard Initializing...');

    // Cache DOM elements
    cacheElements();

    // Initialize components
    initializeClock();
    initializeEventListeners();

    // Start polling
    startPolling();

    console.log('✓ Dashboard Initialized');
});

function cacheElements() {
    elements = {
        // Status
        statusIndicator: document.getElementById('statusIndicator'),
        connectionStatus: document.getElementById('connectionStatus'),

        // Statistics
        totalPackets: document.getElementById('totalPackets'),
        totalAttacks: document.getElementById('totalAttacks'),
        detectionRate: document.getElementById('detectionRate'),

        // Threat panel
        threatContent: document.getElementById('threatContent'),

        // Logs
        logsTableBody: document.getElementById('logsTableBody'),

        // Controls
        btnStart: document.getElementById('btnStart'),
        btnStop: document.getElementById('btnStop'),
        fileUpload: document.getElementById('fileUpload'),
        uploadStatus: document.getElementById('uploadStatus'),
        monitoringState: document.getElementById('monitoringState'),

        // Clock
        liveClock: document.getElementById('liveClock')
    };
}

function initializeClock() {
    updateClock();
    setInterval(updateClock, 1000);
}

function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    elements.liveClock.textContent = `${hours}:${minutes}:${seconds}`;
}

function initializeEventListeners() {
    // Start monitoring button
    elements.btnStart.addEventListener('click', function () {
        controlMonitoring('start');
    });

    // Stop monitoring button
    elements.btnStop.addEventListener('click', function () {
        controlMonitoring('stop');
    });

    // File upload
    elements.fileUpload.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            uploadFile(file);
        }
    });
}

// ===== AJAX Polling =====

function startPolling() {
    if (isPolling) return;

    isPolling = true;
    console.log('📡 Starting real-time polling...');

    // Initial fetch
    fetchStatus();
    fetchLogs();

    // Set up polling interval
    pollingTimer = setInterval(function () {
        fetchStatus();
        fetchLogs();
    }, POLL_INTERVAL);
}

function stopPolling() {
    if (!isPolling) return;

    isPolling = false;
    console.log('⏸️ Stopping polling...');

    if (pollingTimer) {
        clearInterval(pollingTimer);
        pollingTimer = null;
    }
}

function fetchStatus() {
    fetch('/api/status')
        .then(response => {
            if (!response.ok) throw new Error('API request failed');
            return response.json();
        })
        .then(data => {
            updateStatus(data);
            updateConnectionStatus(true);
        })
        .catch(error => {
            console.error('Error fetching status:', error);
            updateConnectionStatus(false);
        });
}

function fetchLogs() {
    fetch('/api/logs?limit=20')
        .then(response => response.json())
        .then(data => {
            updateLogs(data.logs);
        })
        .catch(error => {
            console.error('Error fetching logs:', error);
        });
}

// ===== Update Functions =====

function updateStatus(data) {
    // Update status indicator
    const status = data.status || 'SAFE';
    const statusEl = elements.statusIndicator;

    // Remove all status classes
    statusEl.classList.remove('safe', 'warning', 'danger');

    // Add current status class
    statusEl.classList.add(status.toLowerCase());

    // Update status text and icon
    const statusText = statusEl.querySelector('.status-text');
    const statusIcon = statusEl.querySelector('.status-icon');

    statusText.textContent = status;

    switch (status) {
        case 'SAFE':
            statusIcon.textContent = '🔒';
            break;
        case 'WARNING':
            statusIcon.textContent = '⚠️';
            break;
        case 'DANGER':
            statusIcon.textContent = '🚨';
            break;
    }

    // Update statistics with animation
    animateCounter(elements.totalPackets, data.total_packets || 0);
    animateCounter(elements.totalAttacks, data.total_attacks || 0);
    elements.detectionRate.textContent = `${data.detection_rate || 0}%`;

    // Update last threat
    updateLastThreat(data.last_threat);

    // Update chart
    if (typeof updateChart === 'function') {
        updateChart(data.distribution || { normal: 0, attack: 0 });
    }

    // Update monitoring state
    elements.monitoringState.textContent = data.monitoring_active ? 'Active' : 'Stopped';
    elements.monitoringState.style.color = data.monitoring_active ? '#00ff88' : '#ff3366';
}

function updateLastThreat(threat) {
    if (!threat) {
        elements.threatContent.innerHTML = '<p class="no-threat">No threats detected yet</p>';
        return;
    }

    const html = `
        <div class="threat-details">
            <div class="threat-item">
                <label>Time</label>
                <value>${formatTimestamp(threat.timestamp)}</value>
            </div>
            <div class="threat-item">
                <label>Threat Type</label>
                <value>${threat.threat_type || 'Unknown'}</value>
            </div>
            <div class="threat-item">
                <label>Confidence</label>
                <value>${(threat.confidence * 100).toFixed(1)}%</value>
            </div>
            <div class="threat-item">
                <label>Protocol</label>
                <value>${threat.protocol || 'N/A'}</value>
            </div>
            <div class="threat-item">
                <label>Service</label>
                <value>${threat.service || 'N/A'}</value>
            </div>
        </div>
    `;

    elements.threatContent.innerHTML = html;
}

function updateLogs(logs) {
    if (!logs || logs.length === 0) {
        elements.logsTableBody.innerHTML = '<tr><td colspan="6" class="no-data">No logs available</td></tr>';
        return;
    }

    const rows = logs.map(log => {
        const predictionClass = log.prediction === 'attack' ? 'attack' : 'normal';
        const confidence = (log.confidence * 100).toFixed(1);

        return `
            <tr>
                <td>${formatTimestamp(log.timestamp)}</td>
                <td><span class="prediction-badge ${predictionClass}">${log.prediction}</span></td>
                <td>${confidence}%</td>
                <td>${log.threat_type || '-'}</td>
                <td>${log.protocol_type || '-'}</td>
                <td>${log.service || '-'}</td>
            </tr>
        `;
    }).join('');

    elements.logsTableBody.innerHTML = rows;
}

function updateConnectionStatus(connected) {
    const statusDot = elements.connectionStatus.querySelector('.status-dot');
    const statusText = elements.connectionStatus.querySelector('span:last-child');

    if (connected) {
        statusDot.style.background = '#00ff88';
        statusDot.style.boxShadow = '0 0 20px rgba(0, 255, 136, 0.5)';
        statusText.textContent = 'Connected';
    } else {
        statusDot.style.background = '#ff3366';
        statusDot.style.boxShadow = '0 0 20px rgba(255, 51, 102, 0.5)';
        statusText.textContent = 'Disconnected';
    }
}

// ===== Control Functions =====

function controlMonitoring(action) {
    fetch('/api/control', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ action: action })
    })
        .then(response => response.json())
        .then(data => {
            console.log(`Monitoring ${action}:`, data.message);

            // Show notification
            showNotification(data.message, data.success ? 'success' : 'error');

            // Refresh status
            fetchStatus();
        })
        .catch(error => {
            console.error('Error controlling monitoring:', error);
            showNotification('Failed to control monitoring', 'error');
        });
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    elements.uploadStatus.textContent = 'Uploading...';
    elements.uploadStatus.style.color = '#ffaa00';

    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const msg = `Processed ${data.results.total} packets: ${data.results.normal} normal, ${data.results.attack} attacks`;
                elements.uploadStatus.textContent = msg;
                elements.uploadStatus.style.color = '#00ff88';
                showNotification('File uploaded successfully', 'success');

                // Refresh data
                fetchStatus();
                fetchLogs();
            } else {
                elements.uploadStatus.textContent = 'Upload failed';
                elements.uploadStatus.style.color = '#ff3366';
                showNotification(data.error || 'Upload failed', 'error');
            }

            // Clear file input
            elements.fileUpload.value = '';

            // Clear status after 5 seconds
            setTimeout(() => {
                elements.uploadStatus.textContent = '';
            }, 5000);
        })
        .catch(error => {
            console.error('Error uploading file:', error);
            elements.uploadStatus.textContent = 'Upload error';
            elements.uploadStatus.style.color = '#ff3366';
            showNotification('Upload error', 'error');
        });
}

// ===== Utility Functions =====

function animateCounter(element, targetValue) {
    const currentValue = parseInt(element.textContent) || 0;

    if (currentValue === targetValue) return;

    const duration = 500; // ms
    const steps = 20;
    const increment = (targetValue - currentValue) / steps;
    const stepDuration = duration / steps;

    let current = currentValue;
    let step = 0;

    const timer = setInterval(() => {
        step++;
        current += increment;

        if (step >= steps) {
            element.textContent = targetValue;
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current);
        }
    }, stepDuration);
}

function formatTimestamp(timestamp) {
    if (!timestamp) return '-';

    const date = new Date(timestamp);
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${hours}:${minutes}:${seconds}`;
}

function showNotification(message, type = 'info') {
    console.log(`[${type.toUpperCase()}] ${message}`);
    // Could implement toast notifications here
}

// Export functions for debugging
window.dashboardDebug = {
    startPolling,
    stopPolling,
    fetchStatus,
    fetchLogs
};
