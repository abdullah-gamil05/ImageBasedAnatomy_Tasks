using UnityEngine;

public class RotateObjectSmoothly : MonoBehaviour
{
    private bool isSelected = false; // Is the object selected
    private Quaternion targetRotation; // The target rotation
    private float rotationSpeed = 5f; // The rotation speed

    void Start()
    {
        targetRotation = transform.rotation; // Store the current rotation as the initial target rotation
    }

    void Update()
    {
        // If the object is selected
        if (isSelected)
        {
            HandleRotationInput(); // Process rotation inputs

            // Smoothly rotate towards the target rotation
            transform.rotation = Quaternion.Lerp(transform.rotation, targetRotation, Time.deltaTime * rotationSpeed);
        }
    }

    void OnMouseDown()
    {
        // When the object is clicked, mark it as selected
        isSelected = true;
    }

    void OnMouseUp()
    {
        // When the mouse click is released, deselect the object
        isSelected = false;
    }

    private void HandleRotationInput()
    {
        // Rotate around the Y-axis (left/right)
        if (Input.GetKeyDown(KeyCode.LeftArrow))
        {
            targetRotation *= Quaternion.Euler(0, -90, 0);
        }
        if (Input.GetKeyDown(KeyCode.RightArrow))
        {
            targetRotation *= Quaternion.Euler(0, 90, 0);
        }

        // Rotate around the X-axis (up/down)
        if (Input.GetKeyDown(KeyCode.UpArrow))
        {
            targetRotation *= Quaternion.Euler(-90, 0, 0);
        }
        if (Input.GetKeyDown(KeyCode.DownArrow))
        {
            targetRotation *= Quaternion.Euler(90, 0, 0);
        }

        // Rotate around the Z-axis (Page Up/Page Down)
        if (Input.GetKeyDown(KeyCode.PageUp))
        {
            targetRotation *= Quaternion.Euler(0, 0, 90);
        }
        if (Input.GetKeyDown(KeyCode.PageDown))
        {
            targetRotation *= Quaternion.Euler(0, 0, -90);
        }
    }
}
