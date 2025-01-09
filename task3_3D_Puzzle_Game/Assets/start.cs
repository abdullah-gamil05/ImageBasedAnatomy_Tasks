using UnityEngine;
using UnityEngine.SceneManagement;

public class CubeClickHandler : MonoBehaviour
{
    // Specify the name or index of the scene you want to load
    public string sceneName = "PuzzleGame";

    void OnMouseDown()
    {
        // Load the specified scene when the cube is clicked
        SceneManager.LoadScene(sceneName);
    }
}
