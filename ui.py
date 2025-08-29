import tkinter as tk
from tkinter import ttk, messagebox
from uuid import uuid4
from datetime import datetime
import hashlib

# Initialize party and blockchain classes
party = {'Democratic Party': [], 'Republican Party': [], 'Others': []}


class Voting_Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.users = {}
        self.node_ctr = 1

    def create_voter(self, name):
        uid = self.node_ctr
        self.node_ctr += 1
        self.users[uid] = {'ID': uid, 'Name': name, 'Voted': False, 'Party Voted': None}
        return uid

    def create_vote(self, voter_id, party_name):
        if party_name not in party:
            return "Invalid party!"
        if voter_id not in self.users or self.users[voter_id]['Voted']:
            return "Voter has already voted or is invalid!"
        
        self.transactions.append({
            "Transaction_ID": str(uuid4()).replace("-", ""),
            "Timestamp": datetime.now(),
            "Voter ID": voter_id,
            "Party Name": party_name,
        })
        self.users[voter_id]['Voted'] = True
        self.users[voter_id]['Party Voted'] = party_name
        party[party_name].append(voter_id)

        if len(self.transactions) == 3:
            self.mine_block()
        return "Vote successfully cast!"

    def mine_block(self):
        block = {
            "Header": {
                "Index": len(self.chain) + 1,
                "Timestamp": datetime.now(),
                "ZKP root": "dummy_hash",
                "Previous Hash": self.hash(self.chain[-1]["Header"]) if self.chain else None,
            },
            "Transaction": self.transactions[:3],
        }
        self.chain.append(block)
        del self.transactions[:3]

    def hash(self, block):
        return hashlib.sha256(str(block).encode()).hexdigest()

    def print_blockchain(self):
        return [f"Block {i+1}: {block}" for i, block in enumerate(self.chain)]


blockchain = Voting_Blockchain()

# GUI Setup
app = tk.Tk()
app.title("USA Official Voting Portal")
app.geometry("900x650")
app.resizable(False, False)

# Colors and Fonts
bg_color = "#f0f4fc"
primary_color = "#002868"
secondary_color = "#bf0a30"
text_color = "#000000"  # Changed button text color to black
header_font = ("Helvetica", 22, "bold")
button_font = ("Helvetica", 16, "bold")
label_font = ("Helvetica", 14)
text_font = ("Helvetica", 12)

# Add a header with a logo placeholder
header_frame = tk.Frame(app, bg=bg_color)
header_frame.pack(fill="x")

logo = tk.Label(header_frame, text="🇺🇸", font=("Helvetica", 30), bg=bg_color, fg=primary_color)
logo.pack(side="left", padx=20)

header_label = tk.Label(
    header_frame,
    text="USA Official Voting Portal",
    font=header_font,
    bg=bg_color,
    fg=primary_color,
)
header_label.pack(side="left", pady=10)

# Main Content Frame
main_frame = tk.Frame(app, bg=bg_color)
main_frame.pack(expand=True, fill="both")

tab_control = ttk.Notebook(main_frame)

# Voter Registration Tab
register_tab = tk.Frame(tab_control, bg=bg_color)
tab_control.add(register_tab, text="Register Voter")

tk.Label(register_tab, text="Register a New Voter", font=("Helvetica", 18, "bold"), bg=bg_color, fg=primary_color).pack(pady=10)

divider = tk.Frame(register_tab, height=2, bg=primary_color)
divider.pack(fill="x", pady=10)

voter_name_label = tk.Label(register_tab, text="Voter Name:", font=label_font, bg=bg_color, fg=primary_color)
voter_name_label.pack(pady=10)
voter_name_entry = tk.Entry(register_tab, width=40, font=text_font)
voter_name_entry.pack(pady=5)

def register_voter():
    name = voter_name_entry.get()
    if not name.strip():
        messagebox.showerror("Error", "Voter name cannot be empty!")
    else:
        voter_id = blockchain.create_voter(name)
        messagebox.showinfo("Success", f"Voter registered with ID: {voter_id}")
        voter_name_entry.delete(0, tk.END)

register_button = tk.Button(register_tab, text="Register Voter", font=button_font, bg=secondary_color, fg=text_color, command=register_voter)
register_button.pack(pady=20)

# Cast Vote Tab
vote_tab = tk.Frame(tab_control, bg=bg_color)
tab_control.add(vote_tab, text="Cast Vote")

tk.Label(vote_tab, text="Cast Your Vote", font=("Helvetica", 18, "bold"), bg=bg_color, fg=primary_color).pack(pady=10)

divider = tk.Frame(vote_tab, height=2, bg=primary_color)
divider.pack(fill="x", pady=10)

voter_id_label = tk.Label(vote_tab, text="Voter ID:", font=label_font, bg=bg_color, fg=primary_color)
voter_id_label.pack(pady=10)
voter_id_entry = tk.Entry(vote_tab, width=40, font=text_font)
voter_id_entry.pack(pady=5)

party_label = tk.Label(vote_tab, text="Select Party:", font=label_font, bg=bg_color, fg=primary_color)
party_label.pack(pady=10)
party_dropdown = ttk.Combobox(vote_tab, values=list(party.keys()), state="readonly", font=text_font)
party_dropdown.pack(pady=5)

def cast_vote():
    try:
        voter_id = int(voter_id_entry.get())
        selected_party = party_dropdown.get()
        if not selected_party:
            raise ValueError("No party selected")
        result = blockchain.create_vote(voter_id, selected_party)
        messagebox.showinfo("Result", result)
        voter_id_entry.delete(0, tk.END)
    except ValueError as e:
        messagebox.showerror("Error", str(e))

cast_vote_button = tk.Button(vote_tab, text="Cast Vote", font=button_font, bg=primary_color, fg=text_color, command=cast_vote)
cast_vote_button.pack(pady=20)

# View Blockchain Tab
blockchain_tab = tk.Frame(tab_control, bg=bg_color)
tab_control.add(blockchain_tab, text="View Blockchain")

tk.Label(blockchain_tab, text="Blockchain Records", font=("Helvetica", 18, "bold"), bg=bg_color, fg=primary_color).pack(pady=10)

divider = tk.Frame(blockchain_tab, height=2, bg=primary_color)
divider.pack(fill="x", pady=10)

blockchain_output = tk.Text(blockchain_tab, wrap="word", height=15, width=80, bg="#ffffff", fg="#000", font=text_font)
blockchain_output.pack(pady=10)

def display_blockchain():
    blockchain_output.delete(1.0, tk.END)
    chain_data = blockchain.print_blockchain()
    blockchain_output.insert(tk.END, "\n".join(chain_data))

view_blockchain_button = tk.Button(blockchain_tab, text="Refresh Blockchain", font=button_font, bg=secondary_color, fg=text_color, command=display_blockchain)
view_blockchain_button.pack(pady=20)

# View Party Stats Tab
stats_tab = tk.Frame(tab_control, bg=bg_color)
tab_control.add(stats_tab, text="Party Stats")

tk.Label(stats_tab, text="Party Statistics", font=("Helvetica", 18, "bold"), bg=bg_color, fg=primary_color).pack(pady=10)

divider = tk.Frame(stats_tab, height=2, bg=primary_color)
divider.pack(fill="x", pady=10)

party_stats_label = tk.Label(stats_tab, text="Select Party:", font=label_font, bg=bg_color, fg=primary_color)
party_stats_label.pack(pady=10)
party_stats_dropdown = ttk.Combobox(stats_tab, values=list(party.keys()), state="readonly", font=text_font)
party_stats_dropdown.pack(pady=5)

party_stats_output = tk.Text(stats_tab, wrap="word", height=10, width=80, bg="#ffffff", fg="#000", font=text_font)
party_stats_output.pack(pady=10)

def display_party_stats():
    selected_party = party_stats_dropdown.get()
    if not selected_party:
        messagebox.showerror("Error", "No party selected!")
    else:
        stats = f"Party: {selected_party}\nTotal Votes: {len(party[selected_party])}\nVoters: {party[selected_party]}"
        party_stats_output.delete(1.0, tk.END)
        party_stats_output.insert(tk.END, stats)

view_party_stats_button = tk.Button(stats_tab, text="Show Stats", font=button_font, bg=primary_color, fg=text_color, command=display_party_stats)
view_party_stats_button.pack(pady=20)

# Add tabs to main UI
tab_control.pack(expand=True, fill="both")

# Footer
footer = tk.Label(app, text="© 2024 USA Official Election Portal | Secure Blockchain Voting", font=("Helvetica", 12), bg=primary_color, fg="#ffffff")
footer.pack(side="bottom", fill="x")

# Run the application
app.mainloop()



