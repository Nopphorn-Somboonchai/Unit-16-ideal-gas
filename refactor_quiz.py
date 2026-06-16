import re
import sys

def main():
    file_path = 'h:\\05-Physics\\Unit 16\\Unit 16.1\\index.html'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Update generateQuestionInstance
    content = content.replace(
'''    // สร้างอ็อบเจ็กต์สุ่มปกติสำหรับโหมดฝึกฝน (Practice)
    const practiceRNG = new NormalRNG();

    // ฟังก์ชันตัวช่วยในการสร้างโจทย์และรับประกันความไม่ซ้ำกันของตัวสุ่มพารามิเตอร์
    function generateQuestionInstance(template, rng) {
      if (!rng) return template.generate(null); // กรณีใช้คู่มือครู (สุ่มธรรมดาแบบกำหนดค่าคงที่)
      let instance;
      let attempts = 0;
      const maxAttempts = 100;

      while (attempts < maxAttempts) {
        instance = template.generate(rng);
        const paramStr = JSON.stringify(instance.params);

        // ถ้ายังไม่เคยถูกสร้าง ให้บันทึกลงประวัติและส่งผลลัพธ์กลับทันที
        if (!rng.hasGenerated(template.id, paramStr)) {
          rng.recordGeneration(template.id, paramStr, 15);
          break;
        }
        attempts++;
      }
      return instance;
    }''',
'''    // สร้างอ็อบเจ็กต์สุ่มปกติสำหรับโหมดฝึกฝน (Practice) จะไม่ได้ใช้ในระบบไดนามิกแล้ว แต่คงคลาสเดิมไว้
    
    // ฟังก์ชันตัวช่วยในการสร้างโจทย์แบบแปรผันตามเลขที่ (Dynamic Parameters)
    function generateQuestionInstance(template, R) {
      if (!R) return template.generate(null); // กรณีไม่ได้ส่ง R มา (เช่นดูเฉลยโหมดสุ่มธรรมดา)
      return template.generate(R);
    }''')

    # 2. Update regeneratePractice
    content = content.replace(
'''    function regeneratePractice() {
      const mode = document.getElementById('prac-type-select').value;
      const isRandom = mode === 'random';
      const formattedTopic = currentPracticeTopic.replace(/-/g, '.');
      const filtered = QUESTION_TEMPLATES.filter(q => q.topic === formattedTopic);
      if (filtered.length === 0) return;
      const template = filtered[Math.floor(Math.random() * filtered.length)];
      const instance = generateQuestionInstance(template, isRandom ? practiceRNG : null);''',
'''    function regeneratePractice() {
      const mode = document.getElementById('prac-type-select').value;
      const isRandom = mode === 'random';
      const formattedTopic = currentPracticeTopic.replace(/-/g, '.');
      const filtered = QUESTION_TEMPLATES.filter(q => q.topic === formattedTopic);
      if (filtered.length === 0) return;
      const template = filtered[Math.floor(Math.random() * filtered.length)];
      const R = isRandom ? Math.floor(Math.random() * 40) + 1 : null;
      const instance = generateQuestionInstance(template, R);''')

    # 3. Update startExamProcess
    content = content.replace(
'''      const generatedQuestions = selectedTemplates.map((template) => {
        // ใช้ฟังก์ชันตัวช่วยสุ่มโจทย์แบบไม่ซ้ำ โดยส่งตัวสุ่มแบบ Seeded RNG เข้าไป
        const instance = generateQuestionInstance(template, examRNG);
        return {
          id: template.id, topic: template.topic, type: template.type, title: template.title,
          text: template.text(instance.params), inputs: template.inputs || [], choices: template.choices || [],
          answers: instance.answers, answersRaw: instance.answersRaw, explanationText: instance.explanation()
        };
      });''',
'''      const R = parseInt(num);
      const generatedQuestions = selectedTemplates.map((template) => {
        // ดึงโจทย์โดยส่งเลขที่ (R) ไปผูกกับสูตรโดยตรง
        const instance = generateQuestionInstance(template, R);
        return {
          id: template.id, topic: template.topic, type: template.type, title: template.title,
          text: template.text(instance.params), inputs: template.inputs || [], choices: template.choices || []
          // ไม่บันทึก answers และ answersRaw ลงใน state เพื่อป้องกันการฝังคำตอบแบบ Static (ทำตาม Backend Validation Rule)
        };
      });''')

    # 4. Update submitExam
    content = content.replace(
'''      currentExamQuestions.forEach((q, idx) => {
        let isCorrect = false;
        const userAns = answers[idx];
        if (q.type === 'choice') isCorrect = userAns === q.answers[0];
        else if (q.type === 'numeric_single') isCorrect = userAns && isNumericAnswerCorrect(userAns[0], q.answersRaw[0]);
        else if (q.type === 'numeric_double') isCorrect = userAns && isNumericAnswerCorrect(userAns[0], q.answersRaw[0]) && isNumericAnswerCorrect(userAns[1], q.answersRaw[1]);
        const score = isCorrect ? 2.0 : 0.0;
        total_score += score;
        gradedResults.push({ idx, isCorrect, score, userAns });
      });''',
'''      const R = parseInt(examStudentInfo.number) || 1;
      currentExamQuestions.forEach((q, idx) => {
        let isCorrect = false;
        const userAns = answers[idx];
        const template = QUESTION_TEMPLATES.find(t => t.id === q.id);
        
        // Backend Validation: คำนวณหาเฉลยที่ถูกต้อง On-the-fly ณ เวลานั้น
        const dynamicCalc = template.generate(R);

        if (q.type === 'choice') isCorrect = userAns === dynamicCalc.answers[0];
        else if (q.type === 'numeric_single') isCorrect = userAns && isNumericAnswerCorrect(userAns[0], dynamicCalc.answersRaw[0]);
        else if (q.type === 'numeric_double') isCorrect = userAns && isNumericAnswerCorrect(userAns[0], dynamicCalc.answersRaw[0]) && isNumericAnswerCorrect(userAns[1], dynamicCalc.answersRaw[1]);
        const score = isCorrect ? 2.0 : 0.0;
        total_score += score;
        gradedResults.push({ idx, isCorrect, score, userAns, expectedAnswers: dynamicCalc.answers, explanationText: dynamicCalc.explanation() });
      });''')

    # 5. Update displayExamResults
    content = content.replace(
'''      <div class="text-xs bg-white border border-slate-200 p-2.5 rounded-lg">
        <span>คำตอบของคุณ: <strong class="${grad.isCorrect ? 'text-emerald-600' : 'text-rose-600'}">${userAnsText}</strong></span>
        <br><span>คำตอบที่ถูกต้อง: <strong>${q.answers.join(' หรือ ')}</strong></span>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200 text-xs md:text-sm text-slate-700 space-y-3 math-font">${q.explanationText}</div>''',
'''      <div class="text-xs bg-white border border-slate-200 p-2.5 rounded-lg">
        <span>คำตอบของคุณ: <strong class="${grad.isCorrect ? 'text-emerald-600' : 'text-rose-600'}">${userAnsText}</strong></span>
        <br><span>คำตอบที่ถูกต้อง: <strong>${grad.expectedAnswers.join(' หรือ ')}</strong></span>
      </div>
      <div class="bg-white p-4 rounded-xl border border-slate-200 text-xs md:text-sm text-slate-700 space-y-3 math-font">${grad.explanationText}</div>''')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Replacements done for non-template parts.")

if __name__ == '__main__':
    main()
