/**
 * Environmental Quantum Field Effects - Interactive Visualizations
 * 
 * This script provides interactive Plotly visualizations and collapsible LaTeX/math blocks
 * for the EQFE GitHub Pages site
 * 
 * Author: Justin Todd, justin@pelicansperspective.com
 * Copyright: Pelicans Perspective
 */

// Initialize all visualizations and collapsible elements when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCollapsibleMath();
    initializePlotlyVisualizations();
});

/**
 * Makes all math blocks collapsible
 */
function initializeCollapsibleMath() {
    // Find all math blocks
    const mathBlocks = document.querySelectorAll('.language-math, pre > code.language-math');
    
    // Process each math block
    mathBlocks.forEach((block, index) => {
        const parentElement = block.parentElement;
        const mathContent = block.textContent || block.innerText;
        const uniqueId = `math-block-${index}`;
        
        // Create collapsible container
        const wrapper = document.createElement('div');
        wrapper.className = 'collapsible-math';
        
        // Create toggle button with preview of equation
        const toggleButton = document.createElement('button');
        toggleButton.className = 'math-toggle';
        toggleButton.innerHTML = '<span class="math-preview">' + 
            (mathContent.length > 30 ? mathContent.substring(0, 30) + '...' : mathContent) + 
            '</span> <span class="toggle-icon">+</span>';
        toggleButton.setAttribute('aria-expanded', 'false');
        toggleButton.setAttribute('aria-controls', uniqueId);
        
        // Create content container
        const contentDiv = document.createElement('div');
        contentDiv.className = 'math-content collapsed';
        contentDiv.id = uniqueId;
        // Keep the original math block
        contentDiv.appendChild(block.cloneNode(true));
        
        // Add event listener for toggle
        toggleButton.addEventListener('click', function() {
            const expanded = toggleButton.getAttribute('aria-expanded') === 'true';
            toggleButton.setAttribute('aria-expanded', !expanded);
            contentDiv.classList.toggle('collapsed');
            toggleButton.querySelector('.toggle-icon').textContent = expanded ? '+' : '-';
        });
        
        // Assemble the collapsible structure
        wrapper.appendChild(toggleButton);
        wrapper.appendChild(contentDiv);
        
        // Replace the original element with our collapsible structure
        parentElement.replaceChild(wrapper, block);
    });
}

/**
 * Creates and initializes all Plotly visualizations
 */
function initializePlotlyVisualizations() {
    // Only initialize if we're on a visualization page
    if (!document.querySelector('.visualization-container')) return;
    
    // Field correlation functions
    createFieldCorrelationPlot();
    
    // Temperature effects on correlations
    createTemperatureEffectsPlot();
    
    // Spatial correlation map
    createSpatialCorrelationPlot();
    
    // Amplification mechanism
    createAmplificationProcessPlot();
    
    // Parameter regimes
    createParameterRegimesPlot();
}

/**
 * Creates the field correlation function plots
 */
function createFieldCorrelationPlot() {
    const container = document.getElementById('field-correlation-plot');
    if (!container) return;
    
    // Generate data for different correlation functions
    const tau = Array.from({length: 100}, (_, i) => i * 0.1);
    
    // Heavy field correlation (decays quickly)
    const heavyField = tau.map(t => Math.exp(-t * 2));
    
    // Medium field correlation
    const mediumField = tau.map(t => Math.exp(-t));
    
    // Light field correlation (decays slowly)
    const lightField = tau.map(t => Math.exp(-t * 0.5));
    
    const data = [
        {
            x: tau,
            y: heavyField,
            type: 'scatter',
            mode: 'lines',
            name: 'Heavy Field (Large m)',
            line: {color: 'red', width: 3}
        },
        {
            x: tau,
            y: mediumField,
            type: 'scatter',
            mode: 'lines',
            name: 'Medium Field',
            line: {color: 'blue', width: 3}
        },
        {
            x: tau,
            y: lightField,
            type: 'scatter',
            mode: 'lines',
            name: 'Light Field (Small m)',
            line: {color: 'green', width: 3}
        }
    ];
    
    const layout = {
        title: 'Field Correlation Functions for Different Field Masses',
        xaxis: {title: 'Time Separation (τ)'},
        yaxis: {title: 'Correlation C(τ)'},
        margin: {l: 50, r: 50, t: 50, b: 50},
        legend: {x: 0.7, y: 1},
        annotations: [{
            xref: 'paper',
            yref: 'paper',
            x: 0.5,
            y: -0.15,
            text: 'Drag sliders to adjust parameters',
            showarrow: false
        }]
    };
    
    const config = {responsive: true};
    
    Plotly.newPlot(container, data, layout, config);
    
    // Add sliders for interaction
    addCorrelationControls(container);
}

/**
 * Adds interactive controls for the correlation plots
 */
function addCorrelationControls(container) {
    const controlsDiv = document.createElement('div');
    controlsDiv.className = 'plot-controls';
    controlsDiv.innerHTML = `
        <div class="slider-container">
            <label for="heavy-mass">Heavy Field Mass:</label>
            <input type="range" id="heavy-mass" min="1" max="5" step="0.1" value="2">
            <span id="heavy-mass-value">2.0</span>
        </div>
        <div class="slider-container">
            <label for="medium-mass">Medium Field Mass:</label>
            <input type="range" id="medium-mass" min="0.5" max="3" step="0.1" value="1">
            <span id="medium-mass-value">1.0</span>
        </div>
        <div class="slider-container">
            <label for="light-mass">Light Field Mass:</label>
            <input type="range" id="light-mass" min="0.1" max="1" step="0.05" value="0.5">
            <span id="light-mass-value">0.5</span>
        </div>
    `;
    
    container.parentNode.insertBefore(controlsDiv, container.nextSibling);
    
    // Add event listeners to sliders
    document.getElementById('heavy-mass').addEventListener('input', function(e) {
        const value = parseFloat(e.target.value);
        document.getElementById('heavy-mass-value').textContent = value.toFixed(1);
        updateCorrelationPlot(container);
    });
    
    document.getElementById('medium-mass').addEventListener('input', function(e) {
        const value = parseFloat(e.target.value);
        document.getElementById('medium-mass-value').textContent = value.toFixed(1);
        updateCorrelationPlot(container);
    });
    
    document.getElementById('light-mass').addEventListener('input', function(e) {
        const value = parseFloat(e.target.value);
        document.getElementById('light-mass-value').textContent = value.toFixed(1);
        updateCorrelationPlot(container);
    });
}

/**
 * Updates the correlation plot based on slider values
 */
function updateCorrelationPlot(container) {
    const heavyMass = parseFloat(document.getElementById('heavy-mass').value);
    const mediumMass = parseFloat(document.getElementById('medium-mass').value);
    const lightMass = parseFloat(document.getElementById('light-mass').value);
    
    const tau = Array.from({length: 100}, (_, i) => i * 0.1);
    
    // Update data
    const update = {
        'y': [
            tau.map(t => Math.exp(-t * heavyMass)),
            tau.map(t => Math.exp(-t * mediumMass)),
            tau.map(t => Math.exp(-t * lightMass))
        ]
    };
    
    Plotly.update(container, update, {}, [0, 1, 2]);
}

/**
 * Creates spatial correlation map visualization
 */
function createSpatialCorrelationPlot() {
    const container = document.getElementById('spatial-correlation-plot');
    if (!container) return;
    
    // Create data for heatmaps
    const size = 50;
    const x = Array.from({length: size}, (_, i) => i);
    const y = Array.from({length: size}, (_, i) => i);
    
    // Generate correlation data
    const lowCorrelationZ = [];
    const highCorrelationZ = [];
    
    for (let i = 0; i < size; i++) {
        const lowRow = [];
        const highRow = [];
        for (let j = 0; j < size; j++) {
            // Low correlation is mostly random noise
            lowRow.push(0.2 * Math.random());
            
            // High correlation has a structured pattern
            const centerX = size / 2;
            const centerY = size / 2;
            const distance = Math.sqrt(Math.pow(i - centerX, 2) + Math.pow(j - centerY, 2));
            const radius = size / 3;
            highRow.push(distance < radius ? 0.8 * Math.exp(-distance/radius) + 0.1 * Math.random() : 0.1 * Math.random());
        }
        lowCorrelationZ.push(lowRow);
        highCorrelationZ.push(highRow);
    }
    
    const data = [
        {
            z: lowCorrelationZ,
            type: 'heatmap',
            colorscale: 'Viridis',
            showscale: false,
            name: 'Low Correlation'
        },
        {
            z: highCorrelationZ,
            type: 'heatmap',
            colorscale: 'Viridis',
            showscale: false,
            name: 'High Correlation'
        }
    ];
    
    const layout = {
        grid: {rows: 1, columns: 2, pattern: 'independent'},
        title: 'Spatial Correlation Maps',
        annotations: [
            {
                text: 'Low Correlation Region',
                x: 0.2,
                y: 1.05,
                xref: 'paper',
                yref: 'paper',
                showarrow: false
            },
            {
                text: 'High Correlation Region',
                x: 0.8,
                y: 1.05,
                xref: 'paper',
                yref: 'paper',
                showarrow: false
            }
        ]
    };
    
    const config = {responsive: true};
    
    Plotly.newPlot(container, data, layout, config);
}

/**
 * Creates temperature effects visualization
 */
function createTemperatureEffectsPlot() {
    const container = document.getElementById('temperature-effects-plot');
    if (!container) return;
    
    // Generate data for different temperature correlations
    const tau = Array.from({length: 100}, (_, i) => i * 0.1);
    
    // T = 0 (quantum vacuum)
    const zeroTemp = tau.map(t => Math.exp(-t) + 0.3 * Math.exp(-3 * t) * Math.cos(5 * t));
    
    // T > 0 (thermal)
    const lowTemp = tau.map(t => Math.exp(-1.5 * t) + 0.2 * Math.exp(-3 * t) * Math.cos(5 * t));
    
    // T >> T_opt (high temperature)
    const highTemp = tau.map(t => Math.exp(-2.5 * t) + 0.1 * Math.exp(-4 * t) * Math.cos(5 * t));
    
    const data = [
        {
            x: tau,
            y: zeroTemp,
            type: 'scatter',
            mode: 'lines',
            name: 'T = 0',
            line: {color: 'blue', width: 3}
        },
        {
            x: tau,
            y: lowTemp,
            type: 'scatter',
            mode: 'lines',
            name: 'T > 0',
            line: {color: 'green', width: 3}
        },
        {
            x: tau,
            y: highTemp,
            type: 'scatter',
            mode: 'lines',
            name: 'T >> T_opt',
            line: {color: 'red', width: 3}
        }
    ];
    
    const layout = {
        title: 'Temperature Effects on Field Correlations',
        xaxis: {title: 'Time Separation (τ)'},
        yaxis: {title: 'Correlation C(τ)'},
        margin: {l: 50, r: 50, t: 50, b: 50},
        legend: {x: 0.7, y: 1}
    };
    
    const config = {responsive: true};
    
    Plotly.newPlot(container, data, layout, config);
    
    // Add temperature slider
    const controlsDiv = document.createElement('div');
    controlsDiv.className = 'plot-controls';
    controlsDiv.innerHTML = `
        <div class="slider-container">
            <label for="temperature">Relative Temperature (T/T_opt):</label>
            <input type="range" id="temperature" min="0" max="3" step="0.1" value="1">
            <span id="temperature-value">1.0</span>
        </div>
    `;
    
    container.parentNode.insertBefore(controlsDiv, container.nextSibling);
    
    document.getElementById('temperature').addEventListener('input', function(e) {
        const value = parseFloat(e.target.value);
        document.getElementById('temperature-value').textContent = value.toFixed(1);
        
        // Update correlation functions based on temperature
        const tau = Array.from({length: 100}, (_, i) => i * 0.1);
        
        // Adjust correlation functions based on temperature
        // The higher the temperature, the faster the decay
        const decay1 = 1 + 0.5 * value;
        const decay2 = 1 + 1 * value; 
        const decay3 = 1 + 1.5 * value;
        
        const zeroTemp = tau.map(t => Math.exp(-decay1 * t) + (0.4 - value * 0.1) * Math.exp(-3 * t) * Math.cos(5 * t));
        const lowTemp = tau.map(t => Math.exp(-decay2 * t) + (0.3 - value * 0.1) * Math.exp(-3 * t) * Math.cos(5 * t));
        const highTemp = tau.map(t => Math.exp(-decay3 * t) + (0.2 - value * 0.1) * Math.exp(-4 * t) * Math.cos(5 * t));
        
        const update = {
            'y': [zeroTemp, lowTemp, highTemp]
        };
        
        Plotly.update(container, update, {}, [0, 1, 2]);
    });
}

/**
 * Creates amplification process visualization
 */
function createAmplificationProcessPlot() {
    const container = document.getElementById('amplification-process-plot');
    if (!container) return;
    
    // Create a simple Sankey diagram to illustrate the amplification process
    const data = [{
        type: "sankey",
        orientation: "h",
        node: {
            pad: 15,
            thickness: 20,
            line: {
                color: "black",
                width: 0.5
            },
            label: [
                "Quantum System", 
                "Environmental Field",
                "Quantum Coherence",
                "Field Correlations", 
                "Interference Term",
                "Enhanced Correlations",
                "Decayed Correlations"
            ],
            color: ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]
        },
        link: {
            source: [0, 1, 0, 1, 2, 3, 4, 4],
            target: [2, 3, 4, 4, 5, 5, 5, 6],
            value: [1, 1, 1, 1, 0.7, 0.7, 0.7, 0.3],
            label: ["Generates", "Produces", "Interacts with", "Interacts with", 
                   "Enhancement", "Enhancement", "Enhancement", "Decay"]
        }
    }];

    const layout = {
        title: "Amplification Process Flow",
        font: {
            size: 10
        }
    };

    const config = {responsive: true};
    
    Plotly.newPlot(container, data, layout, config);
}

/**
 * Creates parameter regimes visualization
 */
function createParameterRegimesPlot() {
    const container = document.getElementById('parameter-regimes-plot');
    if (!container) return;
    
    // Generate data for the parameter regime curve (bell-shaped)
    const temp = Array.from({length: 100}, (_, i) => i * 0.1);
    
    // Generate a bell curve for the quantum advantage regime
    const advantage = temp.map(t => {
        const peak = 5;
        const center = 5;
        const width = 2;
        return peak * Math.exp(-Math.pow((t - center), 2) / (2 * Math.pow(width, 2)));
    });
    
    const data = [{
        x: temp,
        y: advantage,
        type: 'scatter',
        mode: 'lines',
        fill: 'tozeroy',
        name: 'Quantum Advantage',
        line: {color: 'rgba(0, 128, 255, 1)', width: 3}
    }];
    
    const layout = {
        title: 'Parameter Regimes for Quantum Advantage',
        xaxis: {
            title: 'Temperature',
            tickvals: [0, 3, 7, 10],
            ticktext: ['0', 'T_min', 'T_max', 'High T']
        },
        yaxis: {
            title: 'Amplification Factor A(φ,t)',
            range: [0, 6]
        },
        annotations: [
            {
                x: 1.5,
                y: 1,
                text: 'Classical Regime',
                showarrow: false,
                font: {size: 14}
            },
            {
                x: 5,
                y: 5.5,
                text: 'Quantum Advantage',
                showarrow: false,
                font: {size: 14}
            },
            {
                x: 8.5,
                y: 1,
                text: 'Decoherence Regime',
                showarrow: false,
                font: {size: 14}
            }
        ],
        shapes: [
            // Dividing lines
            {
                type: 'line',
                x0: 3,
                y0: 0,
                x1: 3,
                y1: 2.5,
                line: {
                    color: 'grey',
                    width: 2,
                    dash: 'dot'
                }
            },
            {
                type: 'line',
                x0: 7,
                y0: 0,
                x1: 7,
                y1: 2.5,
                line: {
                    color: 'grey',
                    width: 2,
                    dash: 'dot'
                }
            }
        ]
    };
    
    const config = {responsive: true};
    
    Plotly.newPlot(container, data, layout, config);
    
    // Add interactive controls
    const controlsDiv = document.createElement('div');
    controlsDiv.className = 'plot-controls';
    controlsDiv.innerHTML = `
        <div class="slider-container">
            <label for="curve-width">Temperature Window Width:</label>
            <input type="range" id="curve-width" min="1" max="4" step="0.1" value="2">
            <span id="curve-width-value">2.0</span>
        </div>
        <div class="slider-container">
            <label for="curve-peak">Peak Amplitude:</label>
            <input type="range" id="curve-peak" min="3" max="8" step="0.5" value="5">
            <span id="curve-peak-value">5.0</span>
        </div>
    `;
    
    container.parentNode.insertBefore(controlsDiv, container.nextSibling);
    
    // Add event listeners to sliders
    document.getElementById('curve-width').addEventListener('input', function(e) {
        const width = parseFloat(e.target.value);
        document.getElementById('curve-width-value').textContent = width.toFixed(1);
        updateParameterPlot(container);
    });
    
    document.getElementById('curve-peak').addEventListener('input', function(e) {
        const peak = parseFloat(e.target.value);
        document.getElementById('curve-peak-value').textContent = peak.toFixed(1);
        updateParameterPlot(container);
    });
}

/**
 * Updates the parameter regime plot based on slider values
 */
function updateParameterPlot(container) {
    const width = parseFloat(document.getElementById('curve-width').value);
    const peak = parseFloat(document.getElementById('curve-peak').value);
    
    const temp = Array.from({length: 100}, (_, i) => i * 0.1);
    
    // Generate updated bell curve
    const advantage = temp.map(t => {
        const center = 5;
        return peak * Math.exp(-Math.pow((t - center), 2) / (2 * Math.pow(width, 2)));
    });
    
    const update = {
        'y': [advantage]
    };
    
    const layoutUpdate = {
        yaxis: {range: [0, peak + 1]},
        annotations: [
            {
                x: 5,
                y: peak + 0.5,
                text: 'Quantum Advantage',
                showarrow: false,
                font: {size: 14}
            }
        ]
    };
    
    Plotly.update(container, update, layoutUpdate, [0]);
}
