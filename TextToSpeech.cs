using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Amazon.Polly;
using Amazon.Runtime;
using Amazon.Polly.Model;
using System.IO;
using UnityEngine.Networking;
using System.Threading.Tasks;

public class TextToSpeech : MonoBehaviour
{
    [SerializeField] private AudioSource audioSource;
    // Start is called before the first frame update


    private async void Start()
    {
        

        var client = new AmazonPollyClient(credentials, Amazon.RegionEndpoint.EUCentral1);
        var request = new SynthesizeSpeechRequest()
        {
            Text = "testing amazon polly on unity",
            Engine = Engine.Neural,
            VoiceId=VoiceId.Kendra,
            OutputFormat=OutputFormat.Mp3
        };
        var response = await client.SynthesizeSpeechAsync(request);
        WriteIntoFile(response.AudioStream);
        using (var www = UnityWebRequestMultimedia.GetAudioClip($"{Application.persistentDataPath}/audio.mp3", AudioType.MPEG))
        {
            var op = www.SendWebRequest();
            while (!op.isDone)
                await Task.Yield();
            var clip = DownloadHandlerAudioClip.GetContent(www);
            audioSource.clip = clip;
            audioSource.Play(); 
        }

        
    }
    private void WriteIntoFile(Stream stream)
    {
        using (var filestream = new FileStream($"{Application.persistentDataPath}/audio.mp3", FileMode.Create))
        {
            byte[] buffer = new byte[4*1024];
            int bytesRead;
            while((bytesRead=stream.Read(buffer, 0, buffer.Length))>0)
            {
                filestream.Write(buffer, 0, bytesRead);
            }
        }
    }

    // Update is called once per frame
    
}
