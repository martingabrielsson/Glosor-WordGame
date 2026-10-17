# Setting up sync between devices (once, about 10 minutes)

The app keeps each week's glosor, and the progress in "Bra ord att kunna!", in a free
Google Firebase database. Every device enters the same **family code** and sees the same data.
Nothing personal is stored, only word lists and progress.

## 1. Create the Firebase project
1. Go to <https://console.firebase.google.com> and sign in with a Google account.
2. **Create a project** (any name, e.g. `glosor`). Turn Google Analytics off.
3. In the left menu: **Build → Firestore Database → Create database**.
   Choose a location in Europe (e.g. `eur3` or `europe-north1`) and **Production mode**.

## 2. Paste these security rules
In Firestore, open the **Rules** tab, replace everything with the text below and press **Publish**.
Only the one shared document (the family code) can be read or written.

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /families/Torpaskolan4A {
      allow get: if true;
      allow create, update: if request.resource.data.keys().hasOnly(['data'])
                            && request.resource.data.data is string
                            && request.resource.data.data.size() < 500000;
      allow list, delete: if false;
    }
  }
}
```

## 3. Get the two values for the app
1. **Project settings** (gear icon) → **General** → under *Your apps* press the **`</>` (Web)** icon,
   give it a name and register it (no hosting needed).
2. Copy the `apiKey` and `projectId` from the config that is shown.

## 4. Put them in the app
In `index.html`, find this line near the top of the script and fill in the values:

```js
const SYNC_CFG = { apiKey: 'AIza...', projectId: 'glosor-12345', code: 'Torpaskolan4A' };
```

Commit and push to GitHub (the app is served by GitHub Pages).

## 5. Use it
Nothing to do on the devices: every device that opens the app link uses the shared code
`Torpaskolan4A` automatically and syncs on its own. **☁️ Synka enheter** shows the status and a
"Synka nu" button.

Notes
- The code is in the (public) repo, so anyone who finds it could read or overwrite the word lists.
  To change it, edit `code` in `SYNC_CFG` **and** the document name in the rules.
- On an iPhone/iPad, Safari and the home-screen icon keep separate data, but both sync to the same shared data.
- Changes sync a couple of seconds after each save, when the app is opened again, and once a minute.
- If two devices change the **same week** at the same time, the most recent change wins.
- Voice speed and sound on/off are per device and not synced.
