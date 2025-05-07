import React, { useState, useEffect } from 'react';
import '../styles/Combat.css';
import { getQuestionsByDifficulty } from '../supabase';

function getRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// Unique races and powerful bosses
const RACES = [
  { name: 'Drakonid', emoji: '🐲', boss: { name: 'Tyrant Varkos', emoji: '🐉', hp: 600, dps: 75 } },
  { name: 'Celestian', emoji: '👼', boss: { name: 'Archangel Seraphiel', emoji: '🕊️', hp: 700, dps: 90 } },
  { name: 'Netherkin', emoji: '👹', boss: { name: 'Dreadlord Malphas', emoji: '🔥', hp: 800, dps: 100 } },
  { name: 'Synthian', emoji: '🤖', boss: { name: 'Prime Unit X-99', emoji: '🛸', hp: 900, dps: 200 } },
  { name: 'Sylvari', emoji: '🌿', boss: { name: 'Ancient Oakenheart', emoji: '🌳', hp: 750, dps: 85 } },
  { name: 'Aquarian', emoji: '🌊', boss: { name: 'Tidebringer Nereus', emoji: '🌊', hp: 650, dps: 95 } },
  { name: 'Pyromancer', emoji: '🔥', boss: { name: 'Inferno Queen Ignis', emoji: '👑', hp: 850, dps: 110 } },
  { name: 'Chronoweaver', emoji: '⌛', boss: { name: 'Temporal Archon', emoji: '🕰️', hp: 950, dps: 120 } }
];


function Combat() {
  // Question pools state
  const [questionPools, setQuestionPools] = useState({
    easy: [],
    medium: [],
    hard: []
  });

  // Load questions on component mount
  useEffect(() => {
    async function loadQuestions() {
      try {
        setLoading(true);
        const easyQuestions = await getQuestionsByDifficulty('easy');
        const mediumQuestions = await getQuestionsByDifficulty('medium');
        const hardQuestions = await getQuestionsByDifficulty('hard');
        
        if (!easyQuestions?.length || !mediumQuestions?.length || !hardQuestions?.length) {
          console.error('Failed to load questions:', { easy: easyQuestions?.length, medium: mediumQuestions?.length, hard: hardQuestions?.length });
          setMessage('Error loading questions. Please refresh the page.');
          return;
        }

        setQuestionPools({
          easy: easyQuestions,
          medium: mediumQuestions,
          hard: hardQuestions
        });
      } catch (error) {
        console.error('Error loading questions:', error);
        setMessage('Error loading questions. Please refresh the page.');
      } finally {
        setLoading(false);
      }
    }
    
    loadQuestions();
  }, []);

  // Separate useEffect for starting battle after questions are loaded
  useEffect(() => {
    if (questionPools.easy.length && questionPools.medium.length && questionPools.hard.length) {
      startBattle();
    }
  }, [questionPools, startBattle, playerLevel, levelPointsHp, playerHealth, timer, gameOver]);

  // Replace static QUESTION_POOLS with dynamic questionPools state
  function getQuestionByDifficulty(difficulty) {
    const pool = questionPools[difficulty];
    if (!pool || pool.length === 0) return null;
    return getRandom(pool);
  }

  // Start new battle
  function startBattle() {
    const diff = getDifficulty();
    const q = getQuestionByDifficulty(diff);
    if (!q) {
      console.error('No questions available for difficulty:', diff);
      setMessage('Error: No questions available. Please refresh the page.');
      setLoading(false);
      return;
    }
    generateEnemy();
    setQuestion(q);
    setPlayerHealth(100 + (playerLevel - 1) * 10 + (levelPointsHp * 10 || 0));
    setMessage('');
    setAnswer('');
    setLoading(false);
    setGameOver(false);
    
    // Timer logic based on difficulty
    let baseTime = diff === 'easy' ? 30 : diff === 'medium' ? 40 : 50;
    setTimeLeft(baseTime);
    if (timer) clearInterval(timer);
    const interval = setInterval(() => {
      setTimeLeft(prev => {
        if (gameOver) {
          clearInterval(interval);
          return prev;
        }
        if (prev <= 1) {
          clearInterval(interval);
          const damage = enemyDps;
          const newPlayerHealth = Math.max(0, playerHealth - damage);
          setPlayerHealth(newPlayerHealth);
          setMessage("Time's up! You took " + damage + ' damage.');
          if (newPlayerHealth <= 0) {
            setGameOver(true);
            setMessage('Game Over! Final Score: ' + score + ' | Level: ' + playerLevel);
          } else {
            startBattle();
          }
          return 0;
        }
        return prev - 0.05;
      });
    }, 200);
    setTimer(interval);
  }

  // Player state
  const [playerLevel, setPlayerLevel] = useState(1);
  const [playerExp, setPlayerExp] = useState(0);
  const [expToNext, setExpToNext] = useState(100);
  const [playerHealth, setPlayerHealth] = useState(100);
  const [playerAttack, setPlayerAttack] = useState(40);
  const [levelPoints, setLevelPoints] = useState(0);

  // Progression state
  const [floor, setFloor] = useState(1);
  const [opponentCount, setOpponentCount] = useState(1);
  const [defeatedTotal, setDefeatedTotal] = useState(0);

  // Enemy state
  const [enemy, setEnemy] = useState({});
  const [enemyHealth, setEnemyHealth] = useState(0);
  const [enemyDps, setEnemyDps] = useState(20);
  const [isBoss, setIsBoss] = useState(false);

  // Question state
  const [question, setQuestion] = useState({});
  const [answer, setAnswer] = useState('');

  // UI/game state
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [gameOver, setGameOver] = useState(false);
  const [score, setScore] = useState(0);
  const [showPointAlloc, setShowPointAlloc] = useState(false);
  const [traits, setTraits] = useState([]); // New: special traits
  const [timer, setTimer] = useState(null); // New: timer for questions
  const [timeLeft, setTimeLeft] = useState(0); // New: time left for answer

  // Calculate current race
  const currentRaceIdx = Math.floor((floor - 1) % RACES.length);
  const currentRace = RACES[currentRaceIdx];

  // Difficulty scaling
  function getDifficulty() {
    if (opponentCount <= 10) return 'easy';
    if (floor < 6) return opponentCount < 8 ? 'medium' : 'hard';
    return opponentCount < 7 ? 'medium' : 'hard';
  }

  // Enemy generator
  function generateEnemy() {
    const boss = opponentCount % 10 === 0;
    setIsBoss(boss);
    if (boss) {
      setEnemy({
        name: currentRace.boss.name,
        emoji: currentRace.boss.emoji,
        health: currentRace.boss.hp + floor * 40,
        flavor: `Boss of Floor ${floor}: ${currentRace.name}`
      });
      setEnemyHealth(currentRace.boss.hp + floor * 40);
      setEnemyDps(currentRace.boss.dps + floor * 5);
    } else {
      setEnemy({
        name: `${currentRace.name} Opponent #${opponentCount}`,
        emoji: currentRace.emoji,
        health: 80 + floor * 18,
        flavor: `A challenger from the ${currentRace.name} race.`
      });
      setEnemyHealth(80 + floor * 18);
      setEnemyDps(20 + floor * 3);
    }
  }

  // Question generator
  
  function generateQuestion() {
    if (gameOver) return; // Don't generate new questions if game is over
    const diff = getDifficulty();
    const q = getQuestionByDifficulty(diff);
    setQuestion(q);
    // Timer logic based on difficulty only
    let baseTime = diff === 'easy' ? 30 : diff === 'medium' ? 40 : 50;
    setTimeLeft(baseTime);
    if (timer) clearInterval(timer);
    const interval = setInterval(() => {
      setTimeLeft(prev => {
        if (gameOver) { // Stop timer if game is over
          clearInterval(interval);
          return prev;
        }
        if (prev <= 1) {
          clearInterval(interval);
          const damage = enemyDps;
          const newPlayerHealth = Math.max(0, playerHealth - damage);
          setPlayerHealth(newPlayerHealth);
          setMessage("Time's up! You took " + damage + " damage.");
          if (newPlayerHealth <= 0) {
            setGameOver(true);
            setMessage('Game Over! Final Score: ' + score + ' | Level: ' + playerLevel);
          } else {
            generateQuestion();
          }
          return 0;
        }
        return prev - 0.5; // Slower countdown
      });
    }, 200); // Update less frequently for slower countdown
    setTimer(interval);
  }

  // Track point allocation
  const [levelPointsHp, setLevelPointsHp] = useState(0);
  const [levelPointsAtk, setLevelPointsAtk] = useState(0);

  // On mount and when floor/opponent changes
  useEffect(() => {
    setLoading(true);
    setTimeout(startBattle, 500);
    // eslint-disable-next-line
  }, [floor, opponentCount]);

  // Handle timeout for question
  function handleTimeout() {
    if (!gameOver && timeLeft === 0) {
      const damage = enemyDps;
      const newPlayerHealth = Math.max(0, playerHealth - damage);
      setPlayerHealth(newPlayerHealth);
      setMessage("Time's up! You took " + damage + " damage.");
      if (newPlayerHealth <= 0) {
        setGameOver(true);
        setMessage('Game Over! Final Score: ' + score + ' | Level: ' + playerLevel);
      } else {
        // Reset timer without generating new question
        const diff = getDifficulty();
        let baseTime = diff === 'easy' ? 30 : diff === 'medium' ? 40 : 50;
        setTimeLeft(baseTime);
        if (timer) clearInterval(timer);
        const interval = setInterval(() => {
          setTimeLeft(prev => {
            if (gameOver) {
              clearInterval(interval);
              return prev;
            }
            if (prev <= 1) {
              clearInterval(interval);
              handleTimeout(); // Call handleTimeout recursively
              return 0;
            }
            return prev - 0.05;
          });
        }, 200);
        setTimer(interval);
      }
    }
  }

  // Handle answer submission
  function handleSubmit(e) {
    e.preventDefault();
    if (timer) clearInterval(timer);
    if (gameOver) {
      // Reset game state on respawn
      setOpponentCount(1);
      setPlayerHealth(100 + (playerLevel - 1) * 10 + (levelPointsHp * 10 || 0));
      setGameOver(false);
      setLoading(true);
      setMessage('Restarted at the beginning of Floor ' + floor + '.');
      setTimeout(startBattle, 500);
      return;
    }
    if (answer.trim().toLowerCase() === question.answer.toLowerCase()) {
      // Correct: damage enemy
      const damage = isBoss ? playerAttack + (levelPointsAtk * 5 || 0) : playerAttack + (levelPointsAtk * 5 || 0);
      const newEnemyHealth = Math.max(0, enemyHealth - damage);
      setEnemyHealth(newEnemyHealth);
      setMessage('Correct! You dealt ' + damage + ' damage.');
      setScore(score + question.points);
      if (newEnemyHealth <= 0) {
        let expGain = isBoss ? 150 : 70;
        setPlayerExp(prev => prev + expGain);
        setDefeatedTotal(prev => prev + 1);
        if (opponentCount % 10 === 0) {
          setFloor(floor + 1);
          setOpponentCount(1);
        } else {
          setOpponentCount(opponentCount + 1);
        }
      } else {
        generateQuestion();
      }
    } else {
      // Incorrect: damage player
      const damage = enemyDps;
      const newPlayerHealth = Math.max(0, playerHealth - damage);
      setPlayerHealth(newPlayerHealth);
      setMessage('Wrong! You took ' + damage + ' damage.');
      if (newPlayerHealth <= 0) {
        setGameOver(true);
        setMessage('Game Over! Final Score: ' + score + ' | Level: ' + playerLevel);
      }
    }
    setAnswer('');
  }

  // Level up logic and point allocation
  useEffect(() => {
    if (playerExp >= expToNext) {
      setPlayerLevel(playerLevel + 1);
      setPlayerExp(playerExp - expToNext);
      setExpToNext(Math.floor(expToNext * 1.35));
      setLevelPoints(prev => prev + 2);
      setShowPointAlloc(true);
      // Add trait every 10 levels
      if ((playerLevel + 1) % 10 === 0) {
        const traitList = [
          'Regeneration: Heal 10 HP after each battle',
          'Critical Strike: +10 Attack vs Bosses',
          'Shield: Take 10 less damage from enemies',
          'Quick Learner: +20% EXP gain',
          'Lucky: 10% chance to avoid damage',
          'Resilience: Survive with 1 HP once per floor',
          'Focus: +5 seconds to answer timer',
          'Power Surge: +20 Attack for next 3 battles'
        ];
        const newTrait = traitList[Math.floor(Math.random() * traitList.length)];
        setTraits(prev => [...prev, newTrait]);
        setMessage('Special Trait Unlocked: ' + newTrait);
      }
    }
    // eslint-disable-next-line
  }, [playerExp]);

  function allocatePoint(stat) {
    if (levelPoints > 0) {
      if (stat === 'hp') {
        setLevelPointsHp(prev => prev + 1);
      } else if (stat === 'atk') {
        setLevelPointsAtk(prev => prev + 1);
        setPlayerAttack(prev => prev + 5);
      }
      setLevelPoints(prev => prev - 1);
      if (levelPoints - 1 === 0) setShowPointAlloc(false);
    }
  }

  if (loading) {
    return (
      <div className="combat-new-loading">
        <div className="combat-new-spinner"></div>
        <p>Loading new battle...</p>
      </div>
    );
  }

  return (
    <div className="combat-new-root">
      <div className="combat-new-main-card">
        <div className="combat-new-enemy-section">
          <div className="combat-new-enemy-img">{enemy.emoji}</div>
          <div className="combat-new-enemy-name">{enemy.name}</div>
          <div className="combat-new-enemy-flavor">{enemy.flavor}</div>
          <div className="combat-new-health-bar enemy">
            <div className="combat-new-health-inner" style={{width: `${(enemyHealth / (enemy.health || 1)) * 100}%`}}></div>
            <span>{enemyHealth} / {enemy.health}</span>
          </div>
        </div>
        <div className="combat-new-vs">VS</div>
        <div className="combat-new-player-section">
          <div className="combat-new-player-img">🧑‍🎓</div>
          <div className="combat-new-player-label">You</div>
          <div className="combat-new-health-bar player">
            <div className="combat-new-health-inner" style={{width: `${playerHealth}%`}}></div>
            <span>{playerHealth} / {100 + (playerLevel - 1) * 10 + (levelPointsHp * 10 || 0)}</span>
          </div>
          <div style={{marginTop: '0.7rem', fontWeight: 600, color: '#1b6ca8'}}>Level {playerLevel}</div>
          <div style={{width: '100%', background: '#e0e0e0', borderRadius: '1rem', height: '0.8rem', marginTop: '0.3rem', position: 'relative'}}>
            <div style={{height: '100%', borderRadius: '1rem', background: 'linear-gradient(90deg,#6c63ff,#43cea2)', width: `${(playerExp/expToNext)*100}%`, transition: 'width 0.5s'}}></div>
            <span style={{position:'absolute',right:'0.7rem',top:'-1.1rem',fontSize:'0.85rem',color:'#333'}}>EXP: {playerExp} / {expToNext}</span>
          </div>
          <div style={{marginTop:'0.5rem',fontWeight:500}}>Attack: {playerAttack + (levelPointsAtk * 5 || 0)}</div>
          <div style={{marginTop:'0.2rem',fontWeight:500}}>Unspent Points: {levelPoints}</div>
          {traits.length > 0 && (
            <div style={{marginTop:'0.5rem',fontWeight:500, color:'#7c3aed'}}>
              Traits: {traits.join(', ')}
            </div>
          )}
        </div>
      </div>
      {showPointAlloc && (
        <div className="combat-new-point-alloc">
          <span className="combat-new-point-title">Level Up! Allocate your points:</span>
          <div className="combat-new-point-buttons">
            <button 
              className={`combat-new-skill-btn ${levelPoints === 0 ? 'disabled' : ''}`}
              onClick={() => allocatePoint('hp')} 
              disabled={levelPoints === 0}
            >
              <span className="skill-icon">❤️</span>
              <span className="skill-text">+10 Max HP</span>
            </button>
            <button 
              className={`combat-new-skill-btn ${levelPoints === 0 ? 'disabled' : ''}`}
              onClick={() => allocatePoint('atk')} 
              disabled={levelPoints === 0}
            >
              <span className="skill-icon">⚔️</span>
              <span className="skill-text">+5 Attack</span>
            </button>
          </div>
        </div>
      )}
      <div className="combat-new-question-card">
        <div className="combat-new-question">{question.text}</div>
        <div style={{fontSize:'0.9rem',color:'#e53e3e',marginBottom:'0.3rem'}}>
          {timeLeft > 0 ? `Time left: ${Math.ceil(timeLeft)}s` : ''}
        </div>
        <form className="combat-new-answer-form" onSubmit={handleSubmit}>
          <input
            className="combat-new-answer-input"
            type="text"
            value={answer}
            onChange={e => setAnswer(e.target.value)}
            placeholder="Type your answer..."
            disabled={gameOver}
            autoFocus
          />
          <button className="combat-new-action-btn" type="submit" disabled={gameOver && !loading}>
            {gameOver ? 'Restart' : isBoss ? 'Fight Boss' : 'Attack'}
          </button>
        </form>
        {message && <div className="combat-new-message">{message}</div>}
      </div>
      <div className="combat-new-footer">
        <span>Floor: {floor}</span>
        <span>Defeated: {defeatedTotal}</span>
        <span>Score: {score}</span>
      </div>
    </div>
  );
}

export default Combat;