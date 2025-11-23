// RoboArm Studio - JavaScript Control
// Robotic arm control interface
// Handles communication with server and user interface

const API_BASE = '';
let isConnected = false;
let currentAngles = [90, 90, 90, 90, 90, 90, 35]; // Initial position (servo 0-5 at 90°, gripper at 35°, range 0-70)
let updateTimeout = null;

// DOM elements
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');
const connectBtn = document.getElementById('connectBtn');
const disconnectBtn = document.getElementById('disconnectBtn');
const portSelect = document.getElementById('portSelect');
const refreshPortsBtn = document.getElementById('refreshPortsBtn');
const sliders = document.querySelectorAll('.slider');

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    // Load available ports
    loadPorts();
    
    // Check initial status
    checkStatus();
    
    // Setup event listeners
    setupEventListeners();
    
    // Load saved positions
    loadSavedPositions();
    
    // Update status every 2 seconds
    setInterval(checkStatus, 2000);
});

function setupEventListeners() {
    // Connection buttons
    connectBtn.addEventListener('click', connectArduino);
    disconnectBtn.addEventListener('click', disconnectArduino);
    refreshPortsBtn.addEventListener('click', loadPorts);
    
    // Servo sliders
    sliders.forEach((slider, index) => {
        slider.addEventListener('input', (e) => {
            const angle = parseInt(e.target.value);
            updateAngleDisplay(index, angle);
        });
        
        slider.addEventListener('change', (e) => {
            let angle = parseInt(e.target.value);
            // Validation: servo 0-5 have range 0-180, gripper (servo 6) has range 0-70
            if (index === 6) {
                angle = Math.max(0, Math.min(70, angle)); // Clamp between 0 and 70 for gripper
            } else {
                angle = Math.max(0, Math.min(180, angle)); // Clamp between 0 and 180 for other servos
            }
            e.target.value = angle; // Update slider if necessary
            moveServo(index, angle);
        });
    });
}

async function loadPorts() {
    try {
        const response = await fetch(`${API_BASE}/api/ports`);
        const data = await response.json();
        
        // Clear select
        portSelect.innerHTML = '<option value="">Auto-detect</option>';
        
        // Add found ports
        data.ports.forEach(port => {
            const option = document.createElement('option');
            option.value = port.device;
            option.textContent = `${port.device} - ${port.description}`;
            portSelect.appendChild(option);
        });
    } catch (error) {
        showNotification('Error loading ports', 'error');
    }
}

async function connectArduino() {
    const port = portSelect.value || null;
    
    connectBtn.disabled = true;
    connectBtn.textContent = 'Connecting...';
    
    try {
        const response = await fetch(`${API_BASE}/api/connect`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ port })
        });
        
        const data = await response.json();
        
        if (data.success) {
            isConnected = true;
            updateConnectionUI(true);
            showNotification('Connected to Arduino!', 'success');
        } else {
            showNotification(data.message || 'Connection failed', 'error');
            connectBtn.disabled = false;
            connectBtn.textContent = 'Connect Arduino';
        }
    } catch (error) {
        showNotification('Connection error', 'error');
        connectBtn.disabled = false;
        connectBtn.textContent = 'Connect Arduino';
    }
}

async function disconnectArduino() {
    try {
        const response = await fetch(`${API_BASE}/api/disconnect`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            isConnected = false;
            updateConnectionUI(false);
            showNotification('Disconnected', 'info');
        }
    } catch (error) {
        // Silent error handling
    }
}

async function checkStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/status`);
        const data = await response.json();
        
        if (data.connected !== isConnected) {
            isConnected = data.connected;
            updateConnectionUI(isConnected);
        }
        
        if (data.angles) {
            currentAngles = data.angles;
            updateAllDisplays();
        }
    } catch (error) {
        // Silent to avoid cluttering console
    }
}

function updateConnectionUI(connected) {
    if (connected) {
        statusIndicator.classList.add('connected');
        statusText.textContent = 'Connected';
        connectBtn.disabled = true;
        disconnectBtn.disabled = false;
        connectBtn.textContent = 'Connected';
    } else {
        statusIndicator.classList.remove('connected');
        statusText.textContent = 'Disconnected';
        connectBtn.disabled = false;
        disconnectBtn.disabled = true;
        connectBtn.textContent = 'Connect Arduino';
    }
}

async function moveServo(servoId, angle) {
    if (!isConnected) {
        showNotification('Arduino not connected!', 'error');
        return;
    }
    
    // Ensure angle is an integer
    angle = parseInt(angle, 10);
    
    // Validation: servo 0-5 have range 0-180, gripper (servo 6) has range 0-70
    if (servoId === 6) {
        angle = Math.max(0, Math.min(70, angle)); // Clamp between 0 and 70 for gripper
    } else {
        angle = Math.max(0, Math.min(180, angle)); // Clamp between 0 and 180 for other servos
    }
    
    // If moving servo 1 (Pin 3), also update servo 2 (Pin 4) in opposite direction
    if (servoId === 1) {
        const oppositeAngle = 180 - angle;
        currentAngles[2] = oppositeAngle;
        // Also update servo 2 slider
        const slider2 = document.getElementById('servo2');
        if (slider2) {
            slider2.value = oppositeAngle;
            updateAngleDisplay(2, oppositeAngle);
        }
    }
    // If moving servo 2 (Pin 4), also update servo 1 (Pin 3) in opposite direction
    else if (servoId === 2) {
        const oppositeAngle = 180 - angle;
        currentAngles[1] = oppositeAngle;
        // Also update servo 1 slider
        const slider1 = document.getElementById('servo1');
        if (slider1) {
            slider1.value = oppositeAngle;
            updateAngleDisplay(1, oppositeAngle);
        }
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ servo: servoId, angle: angle })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentAngles = data.angles;
            
            // Update sliders if there are coupled changes
            if (servoId === 1 || servoId === 2) {
                updateAllDisplays();
            }
        } else {
            showNotification(data.message || 'Movement error', 'error');
        }
    } catch (error) {
        showNotification('Error sending command', 'error');
    }
}

// Load saved positions from server
let savedPositions = {};

async function loadSavedPositions() {
    try {
        const response = await fetch(`${API_BASE}/api/positions`);
        const data = await response.json();
        
        if (data.success) {
            savedPositions = data.positions || {};
            updatePositionsUI();
        }
    } catch (error) {
        console.error('Error loading positions:', error);
    }
}

// Save current slider position
async function savePosition() {
    if (!isConnected) {
        showNotification('Arduino non connesso!', 'error');
        return;
    }
    
    // Get current slider values
    const angles = [];
    sliders.forEach((slider) => {
        angles.push(parseInt(slider.value));
    });
    
    // Ensure servo 1 and 2 are coupled
    angles[2] = 180 - angles[1];
    
    // Ask for position name
    const positionName = prompt('Inserisci un nome per questa posizione:');
    if (!positionName || !positionName.trim()) {
        showNotification('Nome posizione richiesto', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/positions`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: positionName.trim(),
                angles: angles
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            savedPositions = data.positions;
            updatePositionsUI();
            showNotification(`✅ Posizione "${positionName}" salvata!`, 'success');
        } else {
            showNotification(data.message || 'Errore nel salvataggio', 'error');
        }
    } catch (error) {
        showNotification('Errore nel salvataggio', 'error');
    }
}

// Load a saved position
async function loadPosition(positionName) {
    if (!isConnected) {
        showNotification('Arduino non connesso!', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/positions/${encodeURIComponent(positionName)}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentAngles = data.angles;
            updateAllDisplays();
            showNotification(`Posizione "${positionName}" caricata`, 'success');
        } else {
            showNotification(data.message || 'Errore nel caricamento', 'error');
        }
    } catch (error) {
        showNotification('Errore nel caricamento', 'error');
    }
}

// Delete a saved position
async function deletePosition(positionName) {
    if (!confirm(`Sei sicuro di voler eliminare la posizione "${positionName}"?`)) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/positions/${encodeURIComponent(positionName)}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            savedPositions = data.positions;
            updatePositionsUI();
            showNotification(`Posizione "${positionName}" eliminata`, 'success');
        } else {
            showNotification(data.message || 'Errore nell\'eliminazione', 'error');
        }
    } catch (error) {
        showNotification('Errore nell\'eliminazione', 'error');
    }
}

// Align current position with sliders (when manually positioning)
async function alignCurrentPosition() {
    if (!isConnected) {
        showNotification('Arduino non connesso!', 'error');
        return;
    }
    
    // Get values from sliders
    const alignedAngles = [];
    sliders.forEach((slider) => {
        alignedAngles.push(parseInt(slider.value));
    });
    
    // Ensure servo 1 and 2 are coupled
    alignedAngles[2] = 180 - alignedAngles[1];
    
    try {
        const response = await fetch(`${API_BASE}/api/set_current`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ angles: alignedAngles })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentAngles = data.angles;
            updateAllDisplays();
            showNotification('✅ Posizione allineata con gli slider!', 'success');
        } else {
            showNotification(data.message || 'Errore nell\'allineamento', 'error');
        }
    } catch (error) {
        showNotification('Errore nell\'allineamento', 'error');
    }
}

// Update positions UI
function updatePositionsUI() {
    const positionsContainer = document.getElementById('positionsContainer');
    if (!positionsContainer) return;
    
    const positionNames = Object.keys(savedPositions);
    
    if (positionNames.length === 0) {
        positionsContainer.innerHTML = '<p style="color: #666; font-style: italic;">Nessuna posizione salvata. Usa gli slider per posizionare il braccio e clicca "Salva Posizione" per creare una nuova posizione.</p>';
        return;
    }
    
    let html = '<div class="positions-list">';
    positionNames.forEach(name => {
        const position = savedPositions[name];
        const angles = position.angles;
        html += `
            <div class="position-item" style="display: flex; align-items: center; justify-content: space-between; padding: 10px; margin: 5px 0; background: #f5f5f5; border-radius: 5px;">
                <div style="flex: 1;">
                    <strong>${name}</strong>
                    <small style="display: block; color: #666; margin-top: 3px;">
                        ${angles.map((a, i) => `${['Root', 'Arm A1', 'Arm A2', 'Arm B', 'Wrist A', 'Wrist B', 'Gripper'][i]}: ${a}°`).join(' | ')}
                    </small>
                </div>
                <div>
                    <button class="btn btn-small" onclick="loadPosition('${name.replace(/'/g, "\\'")}')" style="margin-right: 5px; background: #2196F3; color: white;">
                        ▶️ Carica
                    </button>
                    <button class="btn btn-small" onclick="deletePosition('${name.replace(/'/g, "\\'")}')" style="background: #f44336; color: white;">
                        🗑️ Elimina
                    </button>
                </div>
            </div>
        `;
    });
    html += '</div>';
    positionsContainer.innerHTML = html;
}

function updateAngleDisplay(servoId, angle) {
    const angleDisplay = document.getElementById(`angle${servoId}`);
    if (angleDisplay) {
        angleDisplay.textContent = `${angle}°`;
    }
}

function updateAllDisplays() {
    // Update sliders
    sliders.forEach((slider, index) => {
        slider.value = currentAngles[index];
        updateAngleDisplay(index, currentAngles[index]);
    });
    
    // Update angle display
    const anglesDisplay = document.getElementById('anglesDisplay');
    const servoNames = ['Root', 'Arm A1', 'Arm A2', 'Arm B', 'Wrist A', 'Wrist B', 'Gripper'];
    
    anglesDisplay.innerHTML = currentAngles.map((angle, index) => 
        `<span>${servoNames[index]}: ${angle}°</span>`
    ).join('');
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Inline styles for notifications
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 25px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    `;
    
    // Colors based on type
    const colors = {
        success: '#4CAF50',
        error: '#f44336',
        info: '#2196F3',
        warning: '#ff9800'
    };
    
    notification.style.background = colors[type] || colors.info;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Utility functions - removed resetAllServo as it used hardcoded preset

function openGripper() {
    if (!isConnected) {
        showNotification('Arduino not connected!', 'error');
        return;
    }
    // Gripper range: 0° = fully open, 70° = fully closed
    moveServo(6, 0); // Full open
    sliders[6].value = 0;
    updateAngleDisplay(6, 0);
}

function closeGripper() {
    if (!isConnected) {
        showNotification('Arduino not connected!', 'error');
        return;
    }
    // Full close at 70°
    moveServo(6, 70); // Full close
    sliders[6].value = 70;
    updateAngleDisplay(6, 70);
}

// Function to bring gripper to rest position (halfway between open and closed)
function resetGripper() {
    if (!isConnected) {
        showNotification('Arduino not connected!', 'error');
        return;
    }
    // Intermediate position between 0° (open) and 70° (closed)
    moveServo(6, 35);
    sliders[6].value = 35;
    updateAngleDisplay(6, 35);
    showNotification('Gripper in rest position', 'info');
}

// Test function to verify critical gripper values
function testGripperRange() {
    if (!isConnected) {
        showNotification('Arduino not connected!', 'error');
        return;
    }
    showNotification('TEST: Verifying critical values (0°=open, 35°=half, 70°=closed)', 'info');
    
    // Sequential test with critical values
    const testValues = [0, 35, 70];
    const testDescriptions = ['FULLY OPEN', 'HALF OPEN', 'FULLY CLOSED'];
    let index = 0;
    let testInterval = setInterval(() => {
        if (index < testValues.length) {
            const angle = testValues[index];
            moveServo(6, angle);
            sliders[6].value = angle;
            updateAngleDisplay(6, angle);
            index++;
        } else {
            clearInterval(testInterval);
            resetGripper(); // Return to center position
            showNotification('Test completed. Verify physical gripper behavior', 'info');
        }
    }, 3000); // 3 seconds per value for better observation
    
    // Allow stopping test by pressing ESC
    const stopTest = (e) => {
        if (e.key === 'Escape') {
            clearInterval(testInterval);
            resetGripper();
            showNotification('Test interrupted', 'info');
            document.removeEventListener('keydown', stopTest);
        }
    };
    document.addEventListener('keydown', stopTest);
}

// Add styles for notification animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
