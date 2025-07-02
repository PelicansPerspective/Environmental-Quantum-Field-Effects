/**
 * EQFE Core JavaScript Functions
 * Handles interactive features for EQFE documentation site
 */

// Preload CSS to avoid flash of unstyled content
document.addEventListener('DOMContentLoaded', function() {
  // Remove content skeleton once everything is loaded
  const contentSkeleton = document.querySelector('.content-skeleton');
  if (contentSkeleton) {
    contentSkeleton.style.opacity = '0';
    setTimeout(() => {
      contentSkeleton.style.display = 'none';
    }, 500);
  }

  // Initialize Plotly interactive visualizations
  initializePlotlyVisualizations();
  
  // Setup collapsible theory sections
  initializeCollapsibleSections();
  
  // Setup poll functionality
  initializePoll();
});

/**
 * Back to Top Button Functionality
 */
function initializeBackToTop() {
  const backToTopButton = document.getElementById("back-to-top");
  if (!backToTopButton) return;
  
  // Show/hide based on scroll position
  window.addEventListener('scroll', function() {
    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
      backToTopButton.style.display = "block";
    } else {
      backToTopButton.style.display = "none";
    }
  });
  
  // Scroll to top with smooth animation
  backToTopButton.addEventListener('click', function() {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

/**
 * Initialize Collapsible Theory Sections
 */
function initializeCollapsibleSections() {
  const collapsibles = document.querySelectorAll('.collapsible-theory');
  
  collapsibles.forEach(function(collapsible) {
    const header = collapsible.querySelector('.collapsible-header');
    const content = collapsible.querySelector('.collapsible-content');
    
    // Initially hide content
    content.style.display = 'none';
    
    // Handle click events
    header.addEventListener('click', function() {
      // Toggle content visibility with animation
      if (content.style.display === 'none' || content.style.display === '') {
        content.style.display = 'block';
        header.querySelector('.toggle-icon i').classList.remove('fa-plus');
        header.querySelector('.toggle-icon i').classList.add('fa-minus');
      } else {
        content.style.display = 'none';
        header.querySelector('.toggle-icon i').classList.remove('fa-minus');
        header.querySelector('.toggle-icon i').classList.add('fa-plus');
      }
    });
  });
}

/**
 * Initialize Plotly Interactive Visualizations
 * This replaces static PNGs with interactive Plotly charts
 */
function initializePlotlyVisualizations() {
  // Environmental Correlation Function Visualization
  const corrPlot = document.getElementById('correlation-function-plot');
  if (corrPlot) {
    // Create interactive correlation function visualization
    const tau = Array.from({length: 100}, (_, i) => (i - 50) * 0.2); // -10 to 10
    
    function calculateCorrelation(tauArr, correlationTime, centralFreq, structure) {
      return tauArr.map(t => {
        const expDecay = Math.exp(-Math.abs(t)/correlationTime);
        const oscillation = Math.cos(centralFreq * t);
        let result = expDecay * oscillation;
        
        // Add structure if requested
        if (structure > 0) {
          const secondFreq = 2.5 * centralFreq;
          const secondDecay = Math.exp(-Math.abs(t)/(0.5 * correlationTime));
          result += structure * secondDecay * Math.cos(secondFreq * t);
        }
        
        return result;
      });
    }
    
    // Initial values
    const corrTime = 1.0;
    const centralFreq = 2.0;
    const structure = 0.0;
    
    const initialCorr = calculateCorrelation(tau, corrTime, centralFreq, structure);
    
    const corrData = [{
      x: tau,
      y: initialCorr,
      type: 'scatter',
      mode: 'lines',
      line: {
        color: '#1a237e',
        width: 3
      },
      name: 'C(τ)'
    }];
    
    const corrLayout = {
      title: 'Environmental Correlation Function C(τ)',
      xaxis: {
        title: 'Time Difference τ'
      },
      yaxis: {
        title: 'Correlation C(τ)'
      },
      margin: {
        l: 50,
        r: 20,
        t: 50,
        b: 50
      }
    };
    
    Plotly.newPlot(corrPlot, corrData, corrLayout, {responsive: true});
    
    // Add controls for interactive parameters
    const controlsDiv = document.createElement('div');
    controlsDiv.className = 'plot-controls';
    controlsDiv.innerHTML = `
      <div class="slider-container">
        <label for="corr-time">Correlation Time (τc):</label>
        <input type="range" id="corr-time" min="0.1" max="5" step="0.1" value="${corrTime}">
        <span>${corrTime}</span>
      </div>
      <div class="slider-container">
        <label for="central-freq">Central Frequency (ω0):</label>
        <input type="range" id="central-freq" min="0" max="5" step="0.1" value="${centralFreq}">
        <span>${centralFreq}</span>
      </div>
      <div class="slider-container">
        <label for="structure">Structure Strength:</label>
        <input type="range" id="structure" min="0" max="1" step="0.1" value="${structure}">
        <span>${structure}</span>
      </div>
    `;
    
    corrPlot.parentNode.appendChild(controlsDiv);
    
    // Add event listeners to update plot
    document.getElementById('corr-time').addEventListener('input', updateCorrelationPlot);
    document.getElementById('central-freq').addEventListener('input', updateCorrelationPlot);
    document.getElementById('structure').addEventListener('input', updateCorrelationPlot);
    
    function updateCorrelationPlot() {
      const newCorrTime = parseFloat(document.getElementById('corr-time').value);
      const newCentralFreq = parseFloat(document.getElementById('central-freq').value);
      const newStructure = parseFloat(document.getElementById('structure').value);
      
      // Update display values
      document.getElementById('corr-time').nextElementSibling.textContent = newCorrTime;
      document.getElementById('central-freq').nextElementSibling.textContent = newCentralFreq;
      document.getElementById('structure').nextElementSibling.textContent = newStructure;
      
      // Calculate new correlation function
      const newCorr = calculateCorrelation(tau, newCorrTime, newCentralFreq, newStructure);
      
      // Update plot
      Plotly.update(corrPlot, {
        'y': [newCorr]
      });
    }
  }
  
  // Enhancement Factor Visualization
  const enhancementPlot = document.getElementById('enhancement-factor-plot');
  if (enhancementPlot) {
    // Create interactive enhancement factor visualization
    const coupling = Array.from({length: 50}, (_, i) => i * 0.1); // 0 to 5
    
    function calculateEnhancement(couplingArr, optCoupling, temp) {
      return couplingArr.map(g => {
        // Simple model of enhancement: g^2 * exp(-g^4/optCoupling^2) * (1 + exp(-temp))
        return 1 + g*g * Math.exp(-Math.pow(g/optCoupling, 4)) * (1 + Math.exp(-temp));
      });
    }
    
    // Initial values
    const optCoupling = 1.5;
    const temp = 1.0;
    
    const initialEnhancement = calculateEnhancement(coupling, optCoupling, temp);
    
    const enhancementData = [{
      x: coupling,
      y: initialEnhancement,
      type: 'scatter',
      mode: 'lines',
      line: {
        color: '#00acc1',
        width: 3
      },
      name: 'Enhancement Factor'
    }];
    
    const enhancementLayout = {
      title: 'Correlation Enhancement Factor',
      xaxis: {
        title: 'Coupling Strength'
      },
      yaxis: {
        title: 'Enhancement Factor'
      },
      margin: {
        l: 50,
        r: 20,
        t: 50,
        b: 50
      }
    };
    
    Plotly.newPlot(enhancementPlot, enhancementData, enhancementLayout, {responsive: true});
    
    // Add controls for interactive parameters
    const controlsDiv = document.createElement('div');
    controlsDiv.className = 'plot-controls';
    controlsDiv.innerHTML = `
      <div class="slider-container">
        <label for="opt-coupling">Optimal Coupling:</label>
        <input type="range" id="opt-coupling" min="0.5" max="3" step="0.1" value="${optCoupling}">
        <span>${optCoupling}</span>
      </div>
      <div class="slider-container">
        <label for="temperature">Temperature (T):</label>
        <input type="range" id="temperature" min="0.1" max="5" step="0.1" value="${temp}">
        <span>${temp}</span>
      </div>
    `;
    
    enhancementPlot.parentNode.appendChild(controlsDiv);
    
    // Add event listeners to update plot
    document.getElementById('opt-coupling').addEventListener('input', updateEnhancementPlot);
    document.getElementById('temperature').addEventListener('input', updateEnhancementPlot);
    
    function updateEnhancementPlot() {
      const newOptCoupling = parseFloat(document.getElementById('opt-coupling').value);
      const newTemp = parseFloat(document.getElementById('temperature').value);
      
      // Update display values
      document.getElementById('opt-coupling').nextElementSibling.textContent = newOptCoupling;
      document.getElementById('temperature').nextElementSibling.textContent = newTemp;
      
      // Calculate new enhancement function
      const newEnhancement = calculateEnhancement(coupling, newOptCoupling, newTemp);
      
      // Update plot
      Plotly.update(enhancementPlot, {
        'y': [newEnhancement]
      });
    }
  }
}

/**
 * Initialize Poll Functionality
 */
function initializePoll() {
  const pollForm = document.getElementById('correlation-poll-form');
  if (!pollForm) return;
  
  pollForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Get selected option
    const selectedOption = document.querySelector('input[name="correlation-type"]:checked');
    if (!selectedOption) {
      alert('Please select an option');
      return;
    }
    
    // In a real implementation, this would send data to a server
    // For now, just show a thank you message
    const pollContainer = document.querySelector('.poll-container');
    pollContainer.innerHTML = `
      <h3>Thank you for your input!</h3>
      <p>We'll consider simulating "${selectedOption.value}" correlation functions in our next update.</p>
    `;
  });
}

// Initialize all functions when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  initializeBackToTop();
  initializeCollapsibleSections();
  initializePlotlyVisualizations();
  initializePoll();
});
