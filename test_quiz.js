const fs = require('fs');

function testQuiz() {
  const html = fs.readFileSync('index.html', 'utf8');
  
  // Extract QUESTION_TEMPLATES
  const templatesMatch = html.match(/const QUESTION_TEMPLATES = \[([\s\S]*?)\];/);
  if (!templatesMatch) {
    console.log("Could not find QUESTION_TEMPLATES");
    return;
  }
  
  // We need to evaluate the templates. Since they use roundHalfEven, formatSci, etc.
  // We'll extract those helper functions as well.
  const helpersMatch = html.match(/(function roundHalfEven[\s\S]*?)const QUESTION_TEMPLATES/);
  
  let script = "";
  if (helpersMatch) {
    script += helpersMatch[1];
  } else {
    // fallback
    script += `
    function roundHalfEven(num, decimals) {
      const p = Math.pow(10, decimals);
      return Math.round(num * p) / p;
    }
    function formatSci(num) { return num.toExponential(2); }
    `;
  }
  
  script += `\nconst QUESTION_TEMPLATES = [${templatesMatch[1]}];\n`;
  script += `
    function generateQuestionInstance(template, R) {
      if (!R) return template.generate(null);
      return template.generate(R);
    }
    
    [1, 15, 40].forEach(R => {
      console.log("\\n--- Testing Roll Number: " + R + " ---");
      QUESTION_TEMPLATES.forEach(t => {
        try {
          const instance = generateQuestionInstance(t, R);
          console.log("Template " + t.id + " success! Answers: " + JSON.stringify(instance.answers));
        } catch (e) {
          console.log("Template " + t.id + " FAILED: " + e.message);
        }
      });
    });
  `;
  
  try {
    eval(script);
  } catch (e) {
    console.error("Eval error:", e);
  }
}

testQuiz();
