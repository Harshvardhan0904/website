function openNav() {
    document.getElementById("mySidebar").style.width = "350px";
  }
function closeNav() {
    document.getElementById("mySidebar").style.width = "0";
  }
  document.getElementById("servicesLink").addEventListener("click", openNav);

  const arr = ['itching', 'skin rash', 'nodal skin eruptions',
    'continuous sneezing', 'shivering', 'chills', 'joint pain',
    'stomach pain', 'acidity', 'ulcers on tongue', 'muscle wasting',
    'vomiting', 'burning micturition', 'spotting  urination',
    'fatigue', 'weight gain', 'anxiety', 'cold hands and feets',
    'mood swings', 'weight loss', 'restlessness', 'lethargy',
    'patches in throat', 'irregular sugar level', 'cough',
    'high fever', 'sunken eyes', 'breathlessness', 'sweating',
    'dehydration', 'indigestion', 'headache', 'yellowish skin',
    'dark urine', 'nausea', 'loss of appetite', 'pain behind the eyes',
    'back pain', 'constipation', 'abdominal pain', 'diarrhoea',
    'mild fever', 'yellow urine', 'yellowing of eyes',
    'acute liver failure', 'fluid overload', 'swelling of stomach',
    'swelled lymph nodes', 'malaise', 'blurred and distorted vision',
    'phlegm', 'throat irritation', 'redness of eyes', 'sinus pressure',
    'runny nose', 'congestion', 'chest pain', 'weakness in limbs',
    'fast heart rate', 'pain during bowel movements',
    'pain in anal region', 'bloody stool', 'irritation in anus',
    'neck pain', 'dizziness', 'cramps', 'bruising', 'obesity',
    'swollen legs', 'swollen blood vessels', 'puffy face and eyes',
    'enlarged thyroid', 'brittle nails', 'swollen extremeties',
    'excessive hunger', 'extra marital contacts',
    'drying and tingling lips', 'slurred speech', 'knee pain',
    'hip joint pain', 'muscle weakness', 'stiff neck',
    'swelling joints', 'movement stiffness', 'spinning movements',
    'loss of balance', 'unsteadiness', 'weakness of one body side',
    'loss of smell', 'bladder discomfort', 'foul smell of urine',
    'continuous feel of urine', 'passage of gases', 'internal itching',
    'toxic look (typhos)', 'depression', 'irritability', 'muscle pain',
    'altered sensorium', 'red spots over body', 'belly pain',
    'abnormal menstruation', 'dischromic  patches',
    'watering from eyes', 'increased appetite', 'polyuria',
    'family history', 'mucoid sputum', 'rusty sputum',
    'lack of concentration', 'visual disturbances',
    'receiving blood transfusion', 'receiving unsterile injections',
    'coma', 'stomach bleeding', 'distention of abdomen',
    'history of alcohol consumption', 'fluid overload.1',
    'blood in sputum', 'prominent veins on calf', 'palpitations',
    'painful walking', 'pus filled pimples', 'blackheads', 'scurring',
    'skin peeling', 'silver like dusting', 'small dents in nails',
    'inflammatory nails', 'blister', 'red sore around nose',
    'yellow crust ooze']

    function populateDatalist(datalistId) {
        const datalist = document.getElementById(datalistId);
        arr.forEach(item => {
            const option = document.createElement("option");
            option.value = item; // Set the value for each option
            datalist.appendChild(option);
        });
    }
    
    // Populate all datalists
    populateDatalist("SymptompOP1");
    populateDatalist("SymptompOP2");
    populateDatalist("SymptompOP3");

    document.addEventListener("DOMContentLoaded", () => {
        populateDatalist("SymptompOP1");
        populateDatalist("SymptompOP2");
        populateDatalist("SymptompOP3");
    });


    function spider(page) {
      const banner = document.querySelector(page);
      const canvas = document.getElementById("dots");
      const ctx = canvas.getContext("2d");
  
      canvas.width = banner.offsetWidth;
      canvas.height = banner.offsetHeight;
  
      let dots = [];
      let breakingDots = []; // Track dots affected by the click
  
      // Generate dots with random positions and velocities
      for (let i = 0; i < 100; i++) {
          dots.push({
              x: Math.random() * canvas.width,
              y: Math.random() * canvas.height,
              size: Math.random() * 3 + 2,
              color: 'rgb(169, 169, 169)',
              vx: (Math.random() - 0.5) * 0.5, // Velocity x
              vy: (Math.random() - 0.5) * 0.5, // Velocity y
          });
      }
  
      let mouse = { x: null, y: null };
  
      // Draw the dots
      const drawDots = () => {
          dots.forEach(dot => {
              ctx.fillStyle = dot.color;
              ctx.beginPath();
              ctx.arc(dot.x, dot.y, dot.size, 0, Math.PI * 2);
              ctx.fill();
          });
      };
  
      // Connect dots within a range
      const connectDots = () => {
          for (let i = 0; i < dots.length; i++) {
              for (let j = i + 1; j < dots.length; j++) {
                  let dx = dots[i].x - dots[j].x;
                  let dy = dots[i].y - dots[j].y;
                  let distance = Math.sqrt(dx * dx + dy * dy);
  
                  if (distance < 150) { // Connection range for dots
                      ctx.strokeStyle = 'rgb(125, 125, 125)';
                      ctx.lineWidth = 0.5;
                      ctx.beginPath();
                      ctx.moveTo(dots[i].x, dots[i].y);
                      ctx.lineTo(dots[j].x, dots[j].y);
                      ctx.stroke();
                  }
                  
              }
          }
      };
  
      // Connect dots to the mouse pointer
      const connectToMouse = () => {
          dots.forEach(dot => {
              let dx = mouse.x - dot.x;
              let dy = mouse.y - dot.y;
              let distance = Math.sqrt(dx * dx + dy * dy);
  
              if (distance < 100) { // Connection range for mouse
                  ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
                  ctx.lineWidth = 1;
                  ctx.beginPath();
                  ctx.moveTo(dot.x, dot.y);
                  ctx.lineTo(mouse.x, mouse.y);
                  ctx.stroke();
              }
              else if (distance < 200) { // Connection range for mouse
                ctx.strokeStyle = 'rgba(0, 213, 255, 0.6)';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(dot.x, dot.y);
                ctx.lineTo(mouse.x, mouse.y);
                ctx.stroke();
                
            }
              
              
          });
      };
  
      // Update dot positions and handle edge collisions
      const updateDots = () => {
          dots.forEach(dot => {
              dot.x += dot.vx;
              dot.y += dot.vy;
  
              // Bounce dots off edges
              if (dot.x < 0 || dot.x > canvas.width) dot.vx *= -1;
              if (dot.y < 0 || dot.y > canvas.height) dot.vy *= -1;
          });
  
          // Handle breaking dots animation
          breakingDots = breakingDots.filter(dot => {
              dot.size -= 0.2; // Shrink dot size
              return dot.size > 0; // Remove dots when size is too small
          });
      };
  
      // Draw breaking effect
      const drawBreakingEffect = () => {
          breakingDots.forEach(dot => {
              ctx.fillStyle = 'rgba(0, 255, 166, 0.8)';
              ctx.beginPath();
              ctx.arc(dot.x, dot.y, dot.size, 0, Math.PI * 2);
              ctx.fill();
          });
      };
  
      // Animation loop
      const animate = () => {
          ctx.clearRect(0, 0, canvas.width, canvas.height);
  
          updateDots();
          drawDots();
          connectDots();
          if (mouse.x !== null && mouse.y !== null) connectToMouse();
          drawBreakingEffect();
  
          requestAnimationFrame(animate);
      };
  
      // Mouse events
      banner.addEventListener("mousemove", (event) => {
          mouse.x = event.pageX - banner.getBoundingClientRect().left;
          mouse.y = event.pageY - banner.getBoundingClientRect().top;
      });
  
      banner.addEventListener("mouseleave", () => {
          mouse.x = null;
          mouse.y = null;
      });
  
      banner.addEventListener("click", (event) => {
          let clickX = event.pageX - banner.getBoundingClientRect().left;
          let clickY = event.pageY - banner.getBoundingClientRect().top;
  
          dots.forEach(dot => {
              let dx = clickX - dot.x;
              let dy = clickY - dot.y;
              let distance = Math.sqrt(dx * dx + dy * dy);
  
              if (distance < 200) { // Break lines for dots within 200 range
                  breakingDots.push({ ...dot, size: 5 }); // Add to breaking effect
              }
          });
      });
  
      // Start animation
      animate();
  }
  
  spider("#main");


document.getElementById("pdf").addEventListener("click",function(){
    alert("Underr Construction")
})