import React, { useState, useEffect } from 'react';

const API_BASE_URL = 'http://127.0.0.1:8001';

const HiraganaGame = () => {
  const [currentChar, setCurrentChar] = useState(null);
  const [userInput, setUserInput] = useState('');
  const [score, setScore] = useState(0);
  const [feedback, setFeedback] = useState('');
  const [error, setError] = useState(null);
  const [uniqueChars, setUniqueChars] = useState(new Set());
  const [showAnswer, setShowAnswer] = useState(false);
  const [attempts, setAttempts] = useState(0);
  const [progress, setProgress] = useState({
    hiragana_progress: { seen: 0, total: 0, percentage: 0, needs_review: 0 },
    katakana_progress: { seen: 0, total: 0, percentage: 0, needs_review: 0 }
  });

  const fetchProgress = () => {
    fetch(`${API_BASE_URL}/api/progress/`)
      .then(response => response.json())
      .then(data => {
        setProgress(data);
      })
      .catch(error => {
        console.error('Error fetching progress:', error);
      });
  };

  const fetchNewCharacter = () => {
    console.log('Fetching new character...');
    setFeedback('');
    fetch(`${API_BASE_URL}/api/random/`)
      .then(response => {
        console.log('Response status:', response.status);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Received character:', data);
        setCurrentChar(data);
        setUniqueChars(prev => new Set([...prev, data.character]));
        setError(null);
        setShowAnswer(false);
        setAttempts(0);
      })
      .catch(error => {
        console.error('Error fetching character:', error);
        setError('Failed to load character. Please try again.');
      });
  };

  useEffect(() => {
    fetchNewCharacter();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!currentChar) return;

    fetch(`${API_BASE_URL}/api/check/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        character_id: currentChar.id,
        answer: userInput,
        was_revealed: false
      })
    })
    .then(response => response.json())
    .then(data => {
      if (data.correct) {
        setScore(score + 1);
        setFeedback('Correct! 🎉');
        fetchProgress();
        setTimeout(() => {
          fetchNewCharacter();
          setUserInput('');
        }, 1000);
      } else {
        setAttempts(prev => prev + 1);
        setFeedback('Not quite right. Try again or reveal the answer:');
        setUserInput('');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      setError('Failed to check answer. Please try again.');
    });
  };

  const handleReveal = () => {
    setShowAnswer(true);
    setFeedback(`The correct answer is: ${currentChar.romaji}`);
    
    // Mark this character as revealed
    fetch(`${API_BASE_URL}/api/check/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        character_id: currentChar.id,
        answer: currentChar.romaji,
        was_revealed: true
      })
    })
    .catch(error => {
      console.error('Error marking as revealed:', error);
    });
  };

  const handleNext = () => {
    fetchNewCharacter();
    setUserInput('');
    setShowAnswer(false);
    setAttempts(0);
    fetchProgress();
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Japanese Learning Game</h1>
      <div style={styles.stats}>
        <div style={styles.scoreBoard}>Score: {score}</div>
        <div style={styles.uniqueChars}>Unique Characters Learned: {uniqueChars.size}</div>
        {attempts > 0 && (
          <div style={styles.attempts}>Attempts: {attempts}</div>
        )}
      </div>

      <div style={styles.progressContainer}>
        <div style={styles.progressBar}>
          <div style={styles.progressLabel}>
            Hiragana Progress: {progress.hiragana_progress.seen}/{progress.hiragana_progress.total} 
            ({progress.hiragana_progress.percentage}%)
            {progress.hiragana_progress.needs_review > 0 && 
              <span style={styles.reviewCount}> - {progress.hiragana_progress.needs_review} need review</span>
            }
          </div>
          <div style={styles.progressBarOuter}>
            <div 
              style={{
                ...styles.progressBarInner,
                width: `${progress.hiragana_progress.percentage}%`
              }}
            />
          </div>
        </div>
        <div style={styles.progressBar}>
          <div style={styles.progressLabel}>
            Katakana Progress: {progress.katakana_progress.seen}/{progress.katakana_progress.total}
            ({progress.katakana_progress.percentage}%)
            {progress.katakana_progress.needs_review > 0 && 
              <span style={styles.reviewCount}> - {progress.katakana_progress.needs_review} need review</span>
            }
          </div>
          <div style={styles.progressBarOuter}>
            <div 
              style={{
                ...styles.progressBarInner,
                width: `${progress.katakana_progress.percentage}%`,
                backgroundColor: '#FF9800'
              }}
            />
          </div>
        </div>
      </div>
      
      {error && <div style={styles.error}>{error}</div>}
      
      {currentChar ? (
        <div style={styles.gameArea}>
          <div style={styles.characterContainer}>
            <div style={styles.character}>{currentChar.character}</div>
            <div style={styles.characterType}>
              {currentChar.character_type.charAt(0).toUpperCase() + currentChar.character_type.slice(1)}
              {currentChar.needs_review && <span style={styles.reviewBadge}>Needs Review</span>}
            </div>
          </div>
          {!showAnswer && (
            <>
              <form onSubmit={handleSubmit} style={styles.form}>
                <input
                  type="text"
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  placeholder="Type the romaji..."
                  style={styles.input}
                  autoFocus
                />
                <button type="submit" style={styles.button}>
                  Check Answer
                </button>
              </form>
              {attempts > 0 && (
                <button onClick={handleReveal} style={styles.revealButton}>
                  Reveal Answer
                </button>
              )}
            </>
          )}
          <div style={styles.feedback}>
            {feedback}
            {showAnswer && (
              <div style={styles.nextButtonContainer}>
                <button onClick={handleNext} style={styles.nextButton}>
                  Next Character →
                </button>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div style={styles.loading}>Loading...</div>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '20px',
    textAlign: 'center',
    fontFamily: 'Arial, sans-serif'
  },
  title: {
    color: '#333',
    marginBottom: '20px'
  },
  stats: {
    display: 'flex',
    justifyContent: 'space-around',
    marginBottom: '20px',
  },
  scoreBoard: {
    fontSize: '1.2em',
    color: '#666'
  },
  uniqueChars: {
    fontSize: '1.2em',
    color: '#666'
  },
  attempts: {
    fontSize: '1.2em',
    color: '#666'
  },
  progressContainer: {
    marginBottom: '30px',
    padding: '15px',
    backgroundColor: '#f5f5f5',
    borderRadius: '8px'
  },
  progressBar: {
    marginBottom: '15px'
  },
  progressLabel: {
    textAlign: 'left',
    marginBottom: '5px',
    color: '#666',
    fontSize: '1em'
  },
  progressBarOuter: {
    width: '100%',
    height: '20px',
    backgroundColor: '#e0e0e0',
    borderRadius: '10px',
    overflow: 'hidden'
  },
  progressBarInner: {
    height: '100%',
    backgroundColor: '#4CAF50',
    transition: 'width 0.3s ease-in-out'
  },
  gameArea: {
    marginTop: '20px'
  },
  characterContainer: {
    marginBottom: '20px'
  },
  character: {
    fontSize: '72px',
    color: '#444'
  },
  characterType: {
    fontSize: '1em',
    color: '#666',
    marginTop: '5px'
  },
  form: {
    marginBottom: '15px'
  },
  input: {
    padding: '10px',
    fontSize: '16px',
    marginRight: '10px',
    borderRadius: '4px',
    border: '1px solid #ddd',
    width: '150px'
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  feedback: {
    marginTop: '20px',
    fontSize: '18px',
    color: '#666'
  },
  error: {
    color: 'red',
    marginBottom: '20px'
  },
  loading: {
    fontSize: '18px',
    color: '#666'
  },
  revealButton: {
    padding: '8px 16px',
    fontSize: '16px',
    backgroundColor: '#FF9800',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    marginTop: '10px'
  },
  nextButton: {
    padding: '10px 20px',
    fontSize: '16px',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    marginTop: '10px'
  },
  reviewCount: {
    fontSize: '1em',
    color: '#666',
    marginLeft: '5px'
  },
  reviewBadge: {
    fontSize: '1em',
    color: '#FF9800',
    marginLeft: '5px'
  }
};

export default HiraganaGame;
