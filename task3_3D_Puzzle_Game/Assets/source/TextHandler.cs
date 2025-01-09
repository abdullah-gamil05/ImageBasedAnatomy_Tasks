using TMPro;
using UnityEngine;

public class DisplayText : MonoBehaviour
{
    private TMP_Text text;

    void Start()
    {
        text = GetComponent<TMP_Text>();
    }

    public void SetResult(string result)
    {
        if (text != null)
        {
            text.text = result;
        }
    }
}
