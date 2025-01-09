using UnityEngine;

public class DragAndSnapWithTimer : MonoBehaviour
{
    private Vector3 originalPosition; // The correct position of the object
    private Quaternion originalRotation; // The correct rotation of the object
    private Vector3 randomPosition;   // The random position
    private Quaternion randomRotation; // The random rotation
    private float moveSpeed = 2.0f;   // The movement speed
    private float snapDistance = 1.0f; // The snapping distance
    private float snapSpeed = 5.0f;   // The snapping speed
    private bool isSelected = false;  // Is the object selected
    private bool isSnapped = false;   // Has the object been placed in the correct position

    private static int correctCount = 0; // Counter for objects in the correct position
    private static bool timerStarted = false; // To start the timer
    private static float timerDuration = 300f; // Timer duration (5 minutes)
    private static float timerEndTime;         // Timer end time
    public GameObject resultText;              // The text object to display results (manually linked)

    private static bool gameEnded = false; // To check if the game has ended

    void Start()
    {
        // Store the correct position and rotation
        originalPosition = transform.position;
        originalRotation = transform.rotation;

        // Generate a random position and rotation
        randomPosition = new Vector3(
            Random.Range(-5f, 5f),
            Random.Range(1f, 3f),
            Random.Range(-5f, 5f)
        );

        float[] possibleAngles = { 0f, 90f, 180f, 270f };
        randomRotation = Quaternion.Euler(
            possibleAngles[Random.Range(0, possibleAngles.Length)],
            possibleAngles[Random.Range(0, possibleAngles.Length)],
            possibleAngles[Random.Range(0, possibleAngles.Length)]
        );

        // Place the object in the random position and rotation
        transform.position = randomPosition;
        transform.rotation = randomRotation;

        // Start the timer after randomizing object positions
        if (!timerStarted)
        {
            timerStarted = true;
            timerEndTime = Time.time + timerDuration; // Set the timer end time
            correctCount = 0; // Reset the counter
            gameEnded = false; // Reset the game state
        }
    }

    void Update()
    {
        if (gameEnded) return; // If the game has ended, do nothing

        // Start the timer
        if (timerStarted)
        {
            float timeLeft = Mathf.Max(0, timerEndTime - Time.time); // Remaining time
            UpdateTimerDisplay(timeLeft);

            // Check if the timer has expired
            if (timeLeft <= 0 && correctCount < 5)
            {
                EndGame("You Lose");
            }
        }

        // Handle movement when the object is selected
        if (isSelected)
        {
            if (Input.GetKey(KeyCode.A)) transform.position += Vector3.left * moveSpeed * Time.deltaTime;
            if (Input.GetKey(KeyCode.D)) transform.position += Vector3.right * moveSpeed * Time.deltaTime;
            if (Input.GetKey(KeyCode.W)) transform.position += Vector3.up * moveSpeed * Time.deltaTime;
            if (Input.GetKey(KeyCode.S)) transform.position += Vector3.down * moveSpeed * Time.deltaTime;
            if (Input.GetKey(KeyCode.Q)) transform.position += Vector3.forward * moveSpeed * Time.deltaTime;
            if (Input.GetKey(KeyCode.E)) transform.position += Vector3.back * moveSpeed * Time.deltaTime;
        }

        // Gradual magnetic snapping
        if (!isSnapped && Vector3.Distance(transform.position, originalPosition) < snapDistance)
        {
            transform.position = Vector3.Lerp(transform.position, originalPosition, snapSpeed * Time.deltaTime);

            if (Vector3.Distance(transform.position, originalPosition) < 0.01f) // If the object has reached the correct position
            {
                transform.position = originalPosition; // Fix the object in place
                transform.rotation = originalRotation; // Fix the object rotation
                isSnapped = true;                      // Mark it as placed
                correctCount++;                        // Increment the counter
                CheckWin();                            // Check for a win
            }
        }
    }

    void OnMouseDown() => isSelected = true;
    void OnMouseUp() => isSelected = false;

    void CheckWin()
    {
        if (correctCount == 5) // Check if all objects are in the correct position
        {
            EndGame("You Win");
        }
    }

    void EndGame(string result)
    {
        gameEnded = true;  // Mark the game as ended
        timerStarted = false;
        DisplayResult(result);
    }

    void DisplayResult(string result)
    {
        if (resultText != null)
        {
            var textScript = resultText.GetComponent<DisplayText>();
            if (textScript != null)
            {
                textScript.SetResult(result);
            }
        }
    }

    void UpdateTimerDisplay(float timeLeft)
    {
        if (resultText != null)
        {
            var textScript = resultText.GetComponent<DisplayText>();
            if (textScript != null)
            {
                int minutes = Mathf.FloorToInt(timeLeft / 60f);
                int seconds = Mathf.FloorToInt(timeLeft % 60f);
                textScript.SetResult($"Time Left: {minutes:00}:{seconds:00}");
            }
        }
    }

    public void ResetPosition()
    {
        transform.position = randomPosition; // Reset the object to its random position
        transform.rotation = randomRotation; // Reset the object to its random rotation
        isSnapped = false;  // Reset the object's state to "not placed"
    }
}
