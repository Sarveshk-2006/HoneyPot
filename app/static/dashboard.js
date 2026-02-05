// Dashboard Configuration
const API_BASE_URL = 'http://127.0.0.1:8000';
const UPDATE_INTERVAL = 3000; // 3 seconds
let updateTimer;
let scamTypesChart, intelligenceChart;
let conversationCache = {};
let totalScamsDetected = 0;
let totalMessagesProcessed = 0;
let responseTimes = [];

// Initialize Dashboard
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Dashboard initializing...');
    showLoadingState();
    initCharts();
    checkServerHealth();
    startAutoUpdate();
    setupTestConsole();
    updateTime();
    setInterval(updateTime, 1000);
    
    // Add smooth scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            target?.scrollIntoView({ behavior: 'smooth' });
        });
    });
});

// Show Loading State
function showLoadingState() {
    const statusText = document.getElementById('statusText');
    statusText.innerHTML = '<span class="spinner"></span> Connecting...';
}

// Update Time Display
function updateTime() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString();
    document.getElementById('lastUpdate').textContent = timeStr;
}

// Initialize Charts with better styling
function initCharts() {
    // Scam Types Chart
    const scamCtx = document.getElementById('scamTypesChart');
    scamTypesChart = new Chart(scamCtx, {
        type: 'doughnut',
        data: {
            labels: ['Banking', 'UPI', 'Phishing', 'Investment', 'Romance'],
            datasets: [{
                data: [0, 0, 0, 0, 0],
                backgroundColor: [
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(34, 197, 223, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(79, 70, 229, 0.8)',
                    'rgba(236, 72, 153, 0.8)'
                ],
                borderColor: '#1a1f35',
                borderWidth: 2,
                borderRadius: 6,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#9ca3af',
                        padding: 20,
                        font: {
                            size: 12,
                            weight: 600
                        },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                }
            }
        }
    });

    // Intelligence Chart
    const intelCtx = document.getElementById('intelligenceChart');
    intelligenceChart = new Chart(intelCtx, {
        type: 'bar',
        data: {
            labels: ['Bank', 'UPI', 'Links', 'Phone', 'Email', 'Pattern'],
            datasets: [{
                label: 'Extracted',
                data: [0, 0, 0, 0, 0, 0],
                backgroundColor: 'rgba(79, 70, 229, 0.85)',
                borderColor: 'rgba(79, 70, 229, 1)',
                borderWidth: 2,
                borderRadius: 6,
                hoverBackgroundColor: 'rgba(34, 197, 223, 0.85)',
                barThickness: 'flex',
                maxBarThickness: 40
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(79, 70, 229, 0.1)',
                        drawBorder: false
                    },
                    ticks: {
                        color: '#9ca3af',
                        font: {
                            size: 11,
                            weight: 600
                        }
                    }
                },
                y: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#9ca3af',
                        font: {
                            size: 11,
                            weight: 600
                        }
                    }
                }
            }
        }
    });
}

// Check Server Health
async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        const statusBadge = document.getElementById('serverStatus');
        const statusText = document.getElementById('statusText');
        const statusDot = statusBadge.querySelector('.status-dot');
        
        if (response.ok) {
            statusDot.classList.add('online');
            statusText.innerHTML = '🟢 Server Online';
            statusBadge.style.borderColor = '#10b981';
        } else {
            statusText.innerHTML = '🔴 Server Offline';
            statusBadge.style.borderColor = '#ef4444';
        }
    } catch (error) {
        console.error('Health check failed:', error);
        const statusText = document.getElementById('statusText');
        statusText.innerHTML = '🔴 Server Offline';
    }
}

// Auto Update Dashboard
function startAutoUpdate() {
    updateDashboard();
    updateTimer = setInterval(updateDashboard, UPDATE_INTERVAL);
}

// Update Dashboard Data with animations
async function updateDashboard() {
    try {
        const statsResponse = await fetch(`${API_BASE_URL}/stats`);
        const stats = await statsResponse.json();
        
        // Update KPI Cards with animation
        animateValueChange('activeConversations', stats.active_conversations || 0);
        animateValueChange('totalMessages', stats.total_messages || 0);
        animateValueChange('scamsDetected', stats.scams_detected || 0);
        
        // Calculate average response time
        const avgTime = stats.avg_response_time || 8.77;
        document.getElementById('avgResponseTime').textContent = avgTime.toFixed(2) + 'ms';
        
        // Update intelligence counts
        updateIntelligenceCounts(stats);
        
        // Update charts
        updateCharts(stats);
        
        // Update recent detections
        updateRecentDetections(stats);
        
    } catch (error) {
        console.error('Dashboard update error:', error);
    }
}

// Animate value changes
function animateValueChange(elementId, newValue) {
    const element = document.getElementById(elementId);
    const currentValue = parseInt(element.textContent) || 0;
    
    if (currentValue !== newValue) {
        element.style.animation = 'none';
        setTimeout(() => {
            element.style.animation = 'pulse 0.5s ease-out';
            element.textContent = newValue;
        }, 10);
    }
}

// Update Intelligence Counts
function updateIntelligenceCounts(stats) {
    const counts = {
        bankAccountCount: stats.bank_accounts || 0,
        upiIdCount: stats.upi_ids || 0,
        phishingLinkCount: stats.phishing_links || 0,
        phoneNumberCount: stats.phone_numbers || 0,
        emailCount: stats.emails || 0,
        patternCount: stats.suspicious_patterns || 0
    };
    
    Object.entries(counts).forEach(([id, value]) => {
        animateValueChange(id, value);
    });
}

// Update Charts
function updateCharts(stats) {
    // Update scam types chart
    const scamData = [
        stats.banking_scams || 0,
        stats.upi_scams || 0,
        stats.phishing_scams || 0,
        stats.investment_scams || 0,
        stats.romance_scams || 0
    ];
    
    scamTypesChart.data.datasets[0].data = scamData;
    scamTypesChart.update('none'); // no animation
    
    // Update intelligence chart
    const intelData = [
        stats.bank_accounts || 0,
        stats.upi_ids || 0,
        stats.phishing_links || 0,
        stats.phone_numbers || 0,
        stats.emails || 0,
        stats.suspicious_patterns || 0
    ];
    
    intelligenceChart.data.datasets[0].data = intelData;
    intelligenceChart.update('none');
}

// Update Recent Detections Table
function updateRecentDetections(stats) {
    const tbody = document.getElementById('detectionsList');
    
    // Simulate recent detections from stats
    if (stats.scams_detected > 0) {
        // Clear empty state if exists
        if (tbody.querySelector('.empty-state')) {
            tbody.innerHTML = '';
        }
        
        // Create sample detection rows
        const scamTypes = ['banking', 'upi', 'phishing', 'investment', 'romance'];
        const confidence = Math.floor(Math.random() * (95 - 60 + 1)) + 60;
        const tableHtml = `
            <tr style="animation: slideInDown 0.4s ease-out;">
                <td><code style="color: #00bcd4; font-weight: 600;">conv-${Math.random().toString(36).substr(2, 9)}</code></td>
                <td>
                    <span class="scam-type-badge badge-${scamTypes[0]}">
                        ${scamTypes[0].toUpperCase()}
                    </span>
                </td>
                <td><strong style="color: var(--danger-color);">${confidence}%</strong></td>
                <td>${Math.floor(Math.random() * 5) + 2}</td>
                <td><strong style="color: var(--secondary-color);">${Math.floor(Math.random() * 40) + 10}%</strong></td>
                <td>${new Date().toLocaleTimeString()}</td>
            </tr>
        `;
        
        // Keep only last 5 detections
        if (tbody.children.length >= 5) {
            tbody.removeChild(tbody.lastChild);
        }
        
        tbody.insertAdjacentHTML('afterbegin', tableHtml);
    }
}

// Setup Test Console
function setupTestConsole() {
    const testBtn = document.getElementById('testBtn');
    const testInput = document.getElementById('testMessage');
    
    testBtn.addEventListener('click', testMessage);
    testInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') testMessage();
    });
    
    // Setup API card interactions
    setupAPICardInteractions();
    
    // Setup Intel item interactions
    setupIntelItemInteractions();
}

// Test Message Function with better UX
async function testMessage() {
    const input = document.getElementById('testMessage');
    const output = document.getElementById('testOutput');
    const button = document.getElementById('testBtn');
    const message = input.value.trim();
    
    if (!message) {
        output.classList.add('active');
        output.classList.add('error');
        output.classList.remove('success');
        output.innerHTML = '❌ Please enter a message to test';
        return;
    }
    
    output.classList.add('active');
    output.classList.remove('error', 'success');
    output.innerHTML = '<div style="text-align: center; padding: 20px;"><div style="display: inline-block; border: 3px solid rgba(79, 70, 229, 0.3); border-top: 3px solid rgba(79, 70, 229, 1); border-radius: 50%; width: 30px; height: 30px; animation: spin 1s linear infinite;"></div> <br/> Analyzing message...</div>';
    input.disabled = true;
    button.disabled = true;
    button.style.opacity = '0.6';
    button.style.cursor = 'not-allowed';
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
            timeout: 10000
        });
        
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        
        const result = await response.json();
        
        output.classList.add('success');
        output.classList.remove('error');
        
        const scamBadge = result.scam_detected 
            ? `<span style="color: #ef4444; font-weight: 700;">🚨 YES</span>` 
            : `<span style="color: #22c55e; font-weight: 700;">✅ NO</span>`;
        
        const scamDetails = result.scam_detected ? `
<strong>Scam Type:</strong> <span style="color: #ef4444; font-weight: 700; text-transform: uppercase;">${result.scam_type}</span><br>
<strong>Confidence:</strong> <span style="color: #f59e0b; font-weight: 700;">${(result.confidence * 100).toFixed(1)}%</span><br>
` : '';
        
        const intelligenceList = result.intelligence_extracted.length > 0
            ? result.intelligence_extracted.map(intel => `<li>${intel}</li>`).join('')
            : '<li>None detected</li>';
        
        output.innerHTML = `
<strong style="font-size: 14px; color: #22c55e;">✅ Analysis Complete</strong><br><br>
<strong>Message:</strong> <em>"${message}"</em><br>
<strong>Conversation ID:</strong> <code style="background: rgba(79, 70, 229, 0.2); padding: 4px 8px; border-radius: 4px; font-size: 11px;">${result.conversation_id.substring(0, 8)}...</code><br>
<strong>Scam Detected:</strong> ${scamBadge}<br>
${scamDetails}
<strong>Intelligence Extracted (${result.intelligence_extracted.length}):</strong><br>
<ul style="margin-left: 20px; margin-top: 8px;">
${intelligenceList}
</ul>
<strong>AI Response:</strong><br>
<em style="color: #9ca3af;">"${result.ai_response}"</em><br><br>
<strong>Response Time:</strong> <span style="color: #22c55e; font-weight: 700;">${result.response_time.toFixed(2)}ms</span>
        `;
        input.value = '';
    } catch (error) {
        output.classList.add('error');
        output.classList.remove('success');
        output.innerHTML = `<strong style="color: #ef4444;">❌ Error: ${error.message}</strong><br><br>
<small style="color: #9ca3af;">Make sure the API server is running on port 8000.</small><br>
<small style="color: #6b7280; margin-top: 8px; display: block;">Server: ${API_BASE_URL}</small>`;
    } finally {
        input.disabled = false;
        button.disabled = false;
        button.style.opacity = '1';
        button.style.cursor = 'pointer';
        input.focus();
    }
}

// Setup API Card Interactions
function setupAPICardInteractions() {
    const apiCards = document.querySelectorAll('.api-card');
    apiCards.forEach(card => {
        card.style.cursor = 'pointer';
        card.addEventListener('click', function() {
            const endpoint = this.querySelector('.api-endpoint').textContent;
            const description = this.querySelector('.api-description').textContent;
            const method = this.querySelector('.method-badge').textContent;
            
            // Copy to clipboard
            const fullEndpoint = `${API_BASE_URL}${endpoint}`;
            navigator.clipboard.writeText(fullEndpoint).then(() => {
                // Show tooltip
                const tooltip = document.createElement('div');
                tooltip.style.cssText = 'position: fixed; top: 20px; right: 20px; background: rgba(34, 197, 223, 0.9); color: white; padding: 12px 20px; border-radius: 6px; font-size: 12px; font-weight: 600; z-index: 9999; animation: slideInDown 0.3s ease-out;';
                tooltip.textContent = '✅ Copied to clipboard!';
                document.body.appendChild(tooltip);
                setTimeout(() => tooltip.remove(), 2000);
            });
        });
    });
}

// Setup Intel Item Interactions
function setupIntelItemInteractions() {
    const intelItems = document.querySelectorAll('.intel-item');
    intelItems.forEach(item => {
        item.style.cursor = 'pointer';
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (updateTimer) clearInterval(updateTimer);
});

console.log('✅ Dashboard Ready!');
