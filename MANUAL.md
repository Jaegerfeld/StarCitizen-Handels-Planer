# SC Trade Planner – Manual

## Quick guide

The Trade Planner shows you which commodity to buy where and where to sell it at a profit. It also keeps a ledger of your cargo, shows where you were after a crash, and estimates your reputation per organisation.

### The tabs

- **Routes:** three lists – Top legal bulk routes (buy stock of 100 SCU or more), Highest margins overall and Illegal routes. With a cargo size chosen you see the outlay and profit per load.
- **All commodities:** every commodity with best buy, best sell and margin. Click a row to see all buy and sell places with price, stock and date.
- **By sell location** and **By buy location:** per place, what you can sell or load there at a profit.
- **Cargo ledger:** which commodity sits in which containers at which station or on which of your ships, with its value.
- **Sessions:** reads the game logs and shows per session the server (shard), last place, last ship and whether the game crashed.
- **Reputation:** estimates your reputation per organisation as a bar to the next rank, after aligning it with your mobiGlas.

### Frequent actions

- Click a column header to sort the table; a second click reverses the order.
- If nothing matches the filters, **Reset filters** clears them.
- **DE | EN** switches the language, **Light / Dark** the colour scheme.
- **What’s new?** shows the changes of the latest versions.
- In the cargo ledger, **Undo** (or Ctrl+Z) reverts the last change.

### Where the data comes from

- Prices, stock and places come from [star-head.de](https://star-head.de). They are maintained by the community and may be days old (column "As of"). Check prices in game before buying.
- Margin/SCU excludes fuel, time and risk.
- The online version is rebuilt every day. **Load latest build (GitHub)** fetches that build, also from an offline copy. Right-click the button to go back to the built-in data.
- The places, commodities and ships in the cargo ledger come from UEX.

### What stays in the browser

- Ledger, alignments, favourites, chosen ship, language and colour scheme are stored only in your browser (localStorage). None of it goes to a server.
- The page reads game logs and screenshots only in the browser. They do not leave your computer.
- A locally opened copy (`SC_Handels_Planer.html`) has its own storage, separate from the online version. What you entered online does not show up there.
- The page also works offline. Only the QR code under **To the phone …**, the text recognition under **Align from screenshots …** and **Load latest build (GitHub)** need the internet.

## Tutorial: Plan a route

Goal: you find a profitable route for your ship and know what a full load costs and earns.

1. Open the **Routes** tab.
2. Under **Cargo**, pick your ship in **Ship** (Cutlass Black, Freelancer or Mercury Star Runner). For another ship, type its SCU into the **SCU** field; the selection then switches to "custom".
3. If needed, narrow **Buy in system** and **Sell in system**, e.g. to the system you are in.
4. Read the list **Top legal bulk routes**. Here the commodity is in stock in quantity at the buy place.
5. Compare the columns **Outlay/load** (the aUEC you need) and **Profit/load** (what is left before costs).
6. If a ⚠ with an SCU number appears next to the profit, the stock at the buy place is smaller than your cargo hold. You will not get a full load there.
7. For a specific commodity or place, type it into **Search (commodity/place)**, e.g. "Gold" or "Levski".
8. For all alternatives, switch to **All commodities**, search the commodity and click its row. Buy places are on the left (cheapest first), sell places on the right (highest first).
9. Check the **As of** column. If the price is old, check it at the terminal in game before you buy.

### Tips

- **Highest margins overall** also contains commodities that only come in tiny amounts. Watch the stock.
- **Illegal routes** only work at hidden terminals. A scan means you lose the cargo and get a CrimeStat.
- For a return load, open **By buy location** and choose your destination under **Buy location**. You then see what you can load there at a profit.
- The browser remembers your chosen ship and SCU.

## Tutorial: Track cargo

Goal: you add your cargo ship, book in the commodity you bought and move it to a station.

1. Open the **Cargo ledger** tab.
2. On the left under **My ships**, click **+ Add ship**.
3. Type the name in **Ship type** and pick it from the list. The list only contains ships with cargo space. You can give it a name under **Own name (optional)**. The ship belongs to your shared fleet: online it also appears with the same name in the **Components** tab of the Ship Purchase Planner, and ships from there (with cargo space) appear here.
4. To track cargo outside the cargo grid, tick **Allow overload (cargo outside the cargo grid)**. The field **Overload up to (% above cargo space)** is set to 33. Then click **Add**.
5. The new ship is selected. In the middle, click **+ Book cargo in**.
6. Choose the **Commodity** from the list, the **Container size** and the **Count**. You can enter the **Buy price per SCU**; the ledger then estimates your profit. Click **Book in**.
7. The cargo appears as a post (e.g. "32 SCU × 4") with its value and best sell place. The ship's fill bar shows how full it is.
8. To move it, drag the post onto a place on the right under **Places** or onto another ship. Or click the post and choose the target in **To**.
9. Enter the amount in the dialog, as **Containers** or in **SCU**, and click **Move**. Remove sold cargo with **Book out**.
10. If your ship takes other container sizes, use **Repack …** in the same dialog, choose the **New container size** and click **Repack**.
11. Unfold the **Journal** at the bottom. Every entry is listed there with its time.
12. At the bottom of the middle column is the **Notes** field. It belongs to the selected place or ship, for example "buy here: 2 × cooler". With nothing selected you write **General notes**. The text is saved as you type; places and ships with a note carry the mark "📝 note" in the lists, and the filter **with cargo or a note only** includes them. The notes are also part of the exports and the storage file.
13. In the [SC Cockpit](https://jaegerfeld.github.io/sc-cockpit/) the same ledger runs in the **Cargo** area. There it also shows the **reminders** at their place, for example purchase reminders from the component planner. If the ledger is open in two tabs, each takes over the other's state as soon as that one saves.

### Tips

- **Find a commodity in the ledger** shows everywhere a commodity sits. Click a result to open that place.
- Warnings (hold full, container too big, illegal, decays) never block you. They only point things out.
- **all sell places ↗** jumps to **All commodities** with this commodity.
- Back up your ledger with **Export JSON** and read it back with **Import JSON**. **Export XLSX** creates an Excel file.
- In Chrome and Edge, **Storage …** also keeps the ledger in a file, e.g. on a USB stick.
- **To the phone …** shows a QR code. The phone takes over your ships and cargo as its ledger.

## Tutorial: Align reputation

Goal: you see per organisation how far you are from the next rank.

1. Open the **Reputation** tab and click **Load log folder …**. Choose the folder `…\Roberts Space Industries\StarCitizen\LIVE` (or `PTU`). If you load the whole LIVE folder, the tab can also show mission texts later.
2. In game, take a screenshot (**Print** key) of the mobiGlas "Reputation" page, one per organisation. A dark background works best, because the mobiGlas is translucent.
3. Click **Align from screenshots …**. Pick the images with **Choose screenshots …** or the whole folder with **Choose folder …** (`StarCitizen\LIVE\screenshots`). You can also drop the images into the dialog.
4. The first time, the page loads the text recognition (a few MB). It then finds the organisation, rank and bar in each image.
5. Check the list. Per row you can untick it or change the organisation. Per organisation the newest image counts.
6. Click the button at the bottom, e.g. **Apply 5 alignments**. The organisations now appear as cards with rank and bar.
7. For a single organisation, click the upper half of its card or ▾. Organisations without an alignment are listed by name under "Not aligned"; a click unfolds the card. Then click **Align with the mobiGlas …**.
8. Let **Read screenshot …** fill in the fields, or enter them yourself: **Rank (highlighted tile)** is your current rank, **Bar of this tile in %** the way to the next rank. Check **Time of the look** and click **Apply**.
9. From the alignment on, the tab adds every mission you complete afterwards from the logs. Load the log folder again after playing.
10. Unfolded, the card shows under **Missions by rank** which missions are unlocked and what comes next.

### Tips

- Align an organisation a second time later. The tab then learns how much reputation a mission really gives there (factor), and the estimate gets more precise.
- Shared missions count as a range (half to full amount). Failed and abandoned missions count 0.
- The star (☆) pins an organisation to the top under **Favourites**.
- **Cards | List** and **Order:** "next rank-up first" quickly show where the next rank is closest.
- A wrong alignment? **Remove last alignment** in the unfolded card.
- **To the phone …** sends rank and bar to your phone by QR code. There you can only view the state.

## FAQ

### Where was I before the crash?

1. Open the **Sessions** tab and click **Load log folder …**.
2. Choose the folder `…\StarCitizen\LIVE` (or `PTU`). Chrome asks "Upload files?"; the files still stay on your computer.
3. At the top you see the card **Last time**, and after a crash also **Last crash**. It shows the shard – with the name the game shows when joining, if known, and the id below –, region, server, **Last place** and **Last ship**.
4. If the last place is an underlined name, a click opens that place in the cargo ledger. **copy** copies the shard id.

### Why do I have to load the log folder every time?

If Star Citizen is installed under `C:\Program Files` (the default), Chrome does not allow lasting access. If it is elsewhere, **Remember folder …** links the folder for good (Chrome and Edge only). The tab reads the newest 25 log files.

### Why do the prices differ from the game?

The prices are reported by the community and may be days old. The **As of** column shows when. Check the price at the terminal before you buy.

### Why does the Reputation tab show no mission texts?

The texts come from the game's language file in the loaded folder. Load the whole LIVE folder with **Load log folder …**, not just `logbackups`, and switch on **Show mission texts**. If the switch is greyed out, clicking it shows the reason.

### How do I move my ledger to another computer?

With **Export JSON** and **Import JSON**, with **Storage …** (Chrome and Edge) through a shared file, or with **To the phone …** to your phone.
