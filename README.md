# AI-Based Assistive Communication Assistant

A Python prototype intended to help people who cannot speak or have difficulty speaking communicate basic needs. It offers:

1. A webcam mode that classifies **custom static hand gestures** into phrases.
2. A touch-based communication board with large phrase buttons and text-to-speech.

## Important scope and safety

- This is an educational prototype, not a clinically validated assistive device.
- The gesture labels are user-defined. They are **not universal ASL signs**.
- Work with the intended user, family and/or speech-language professional to choose gestures that are comfortable, distinct and reliable.
- The first version recognizes static hand poses, not full sign-language grammar or dynamic signs.
- The touch board is available without training a model and is an important alternative input method.
- Emergency phrases are displayed/spoken locally; the app does not call emergency services.
- Never rely on this prototype as the sole means of requesting urgent help.

## Requirements

Recommended: Python 3.11. Create and activate a virtual environment:

### macOS / Linux
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows
```powershell
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

If MediaPipe installation fails, verify that you are using a supported Python 3.11 environment and a compatible computer architecture.

## Start with the touch communication board

This mode does not require webcam access or a trained model:

```bash
streamlit run communication_board.py
```

Select a phrase, then press **SPEAK**. You can also type a custom phrase.

## Set up webcam gesture recognition

### 1. Collect training data

```bash
python collect_data.py
```

The terminal and webcam window show the number-key mapping:
- 1: I need water
- 2: I am hungry
- 3: I need food
- 4: I need help
- 5: I am in pain
- 6: I need the bathroom
- 7: Please call a doctor
- 8: I need my family
- 9: Yes
- 0: No

Show a chosen gesture and hold its number key to save samples. Collect around 100-200 samples per phrase, varying hand position, distance, background and lighting. Press X to deselect and Q to quit.

Use gestures that the intended user can comfortably and consistently make. If a gesture is uncomfortable or ambiguous, choose another. Do not assume that a custom gesture has the same meaning in another sign-language community.

### 2. Train the model

```bash
python train_model.py
```

The trained model is saved to `models/communication_model.pkl`.

### 3. Run webcam mode

```bash
python app.py
```

- S: speak the currently recognized phrase
- C: clear the displayed phrase
- Q: quit

## Project files

- `communication_phrases.py`: phrase vocabulary
- `gesture_utils.py`: consistent 21-point landmark preprocessing
- `collect_data.py`: collect custom gesture examples
- `train_model.py`: train and evaluate Random Forest
- `translator.py`: load model and predict
- `app.py`: webcam interface
- `communication_board.py`: touch-based phrase board

## Model details

MediaPipe extracts 21 3D hand landmarks. Wrist-relative, scale-normalized coordinates form 63 features. A Random Forest classifier predicts one of the collected phrase labels.

The reported test score is only a preliminary random holdout score. Similar frames from the same recording session can leak into both train and test sets. For a meaningful evaluation, collect separate sessions and users, then reserve an entire session/person for testing.

## Suggested improvements

- Add user profiles and customizable phrase sets.
- Add Telugu, Hindi and other language text-to-speech.
- Add larger pictogram buttons, switch access and eye-gaze/alternative access methods.
- Add temporal models for dynamic gestures.
- Conduct usability testing with intended users and caregivers.
