using UnityEngine;
using TMPro;

public class GameManager : MonoBehaviour
{
    public TextMeshProUGUI gameMessage; // Text for displaying messages
    public float gameDuration = 120f;  // Game duration (in seconds)
    private bool gameStarted = false;  // Game start state
    private float timer;               // Game timer
    private int snappedObjects = 0;    // Number of objects placed correctly
    private bool gameEnded = false;    // Game end state

    void Update()
    {
        // If the game hasn't started, check for the Enter key
        if (!gameStarted && Input.GetKeyDown(KeyCode.Return))
        {
            StartGame();
        }

        // If the game has started, update the timer and display messages
        if (gameStarted && !gameEnded)
        {
            timer -= Time.deltaTime;
            gameMessage.text = "Time: " + Mathf.CeilToInt(timer) + "s";

            if (timer <= 0)
            {
                EndGame(false); // Time runs out = lose
            }
        }
    }

    public void StartGame()
    {
        // Start the game
        gameStarted = true;
        timer = gameDuration;
        snappedObjects = 0;
        gameEnded = false;
        gameMessage.text = "Time: " + Mathf.CeilToInt(timer) + "s";
    }

    public void EndGame(bool won)
    {
        gameEnded = true;
        gameStarted = false;

        if (won)
        {
            gameMessage.text = "You Win!";
        }
        else
        {
            gameMessage.text = "You Lose!";
        }
    }

    public void ObjectSnapped()
    {
        // Called when an object is correctly placed
        if (!gameStarted || gameEnded) return;

        snappedObjects++;

        if (snappedObjects >= 5)
        {
            EndGame(true); // Win when 5 objects are placed correctly
        }
    }
}
