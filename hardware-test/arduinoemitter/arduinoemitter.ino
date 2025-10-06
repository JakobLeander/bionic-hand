/*=============================================================================
arduinoemitter.ino
Send a stream of serial numbers from Arduino to a connected computer
Copyright(c) 2025 Jakob Leander
Licensed under the MIT License.
=============================================================================*/
int x;

void setup()
{
    x = 0;
    Serial.begin(9600);
}

void loop()
{
    Serial.println(x);

    x++;

    if (x > 255)
    {
        x = 0;
    }

    delay(10);
}