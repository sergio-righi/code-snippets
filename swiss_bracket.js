class SwissTournament {
  constructor(participants, slots) {
    this.participants = participants.map((participant, i) => ({
      ...participant,
      seed: i + 1,
      wins: 0,
      losses: 0,
      diff: 0,
      buchholz: 0,
      opponents: [],
    }));
    this.slots = slots;
    this.rounds = [];
    this.results = [];
    this.breakpoint = Math.ceil(Math.log2(participants.length)) - 1;
  }

  // Sort participants based on the rules (wins, losses, buchholz, seed)
  sortParticipants() {
    this.participants.sort((a, b) => {
      if (a.wins !== b.wins) return b.wins - a.wins;
      if (a.losses !== b.losses) return a.losses - b.losses;
      if (a.buchholz !== b.buchholz) return b.buchholz - a.buchholz;
      return a.seed - b.seed;
    });
  }

  // Remove participants who have 3 wins or 3 losses
  filterParticipants() {
    return this.participants.filter(
      (p) => p.wins < this.breakpoint && p.losses < this.breakpoint
    );
  }

  sliceArray(data) {
    const grouped = {};

    data.forEach((item) => {
      const key = `${item.wins}-${item.losses}`;
      if (!grouped[key]) {
        grouped[key] = [];
      }
      grouped[key].push(item);
    });

    return Object.values(grouped);
  }

  printRound() {
    if (this.rounds.length === 0) return;
    console.log(
      this.rounds[this.rounds.length - 1].map(
        (item) => `${item.player1.name} vs ${item.player2.name}`
      )
    );
  }

  generateRound() {
    const participants = this.filterParticipants();
    if (participants.length < 2) return; // If no participants are left for pairing, stop.

    console.log(`-------- Round ${this.rounds.length + 1} --------`);
    const round = [];
    const slices = this.sliceArray(participants);

    for (let slice of slices) {
      const length = slice.length;

      if (this.rounds.length === 0) {
        // First round: Pair first half with corresponding participant from second half
        const middle = Math.floor(length / 2);
        for (let i = 0; i < middle; i++) {
          const player1 = slice[i];
          const player2 = slice[middle + i];

          round.push({ player1, player2 });
        }
      } else {
        // Subsequent rounds: Pair first with last, second with second-last, etc.
        const unpaired = [...slice]; // Copy the slice to track unpaired participants.

        while (unpaired.length > 1) {
          const player1 = unpaired[0];
          let player2Index = unpaired.length - 1;

          // Ensure player1 hasn't already faced player2
          while (
            player2Index > 0 &&
            player1.opponents.includes(unpaired[player2Index].name)
          ) {
            player2Index--; // Check the next available player
          }

          if (player2Index > 0) {
            const player2 = unpaired[player2Index];

            // Add valid pair to the round
            round.push({
              player1,
              player2,
            });

            // Remove paired players from the unpaired list
            unpaired.splice(player2Index, 1);
            unpaired.shift(); // Remove player1
          } else {
            // If no valid opponent is found for player1, skip pairing
            unpaired.shift();
          }
        }
      }
    }

    this.rounds.push(round);
  }

  generateDecisionRound() {
    if (this.participants.length % 2 === 0 && this.slots % 2 === 0) return;
    this.sortParticipants();
    console.log(`-------- Decision Round --------`);
    this.rounds.push([
      {
        player1: this.participants[this.slots - 1],
        player2: this.participants[this.slots],
      },
    ]);
    this.printRound();
    this.simulateRound(true);
  }

  calculateBuchholz() {
    this.participants.forEach((participant) => {
      participant.buchholz = participant.opponents.reduce(
        (acc, opponentName) => {
          const opponent = this.participants.find(
            (p) => p.name === opponentName
          );
          if (opponent) {
            acc += opponent.wins - opponent.losses;
          }
          return acc;
        },
        0
      );
    });
  }

  processResults(roundResults) {
    roundResults.forEach((result) => {
      const { won, lost, diff } = result;
      const winner = this.participants.find((p) => p.name === won);
      const loser = this.participants.find((p) => p.name === lost);

      // Update winner's stats
      winner.wins = (winner.wins || 0) + 1;
      winner.diff = (winner.diff || 0) + diff;
      winner.opponents = (winner.opponents || []).concat(loser.name);

      // Update loser's stats
      loser.losses = (loser.losses || 0) + 1;
      loser.diff = (loser.diff || 0) - diff;
      loser.opponents = (loser.opponents || []).concat(winner.name);
    });

    this.calculateBuchholz();
  }

  // Check if the tournament should end
  checkEndCondition() {
    const allFinished = this.participants.every(
      (p) => p.wins === this.breakpoint || p.losses === this.breakpoint
    );
    return allFinished;
  }

  // Create a standings table
  generateStandings() {
    console.log(`-------- Standings --------`);
    this.sortParticipants();
    return this.participants.map((p, index) => ({
      name: p.name,
      wins: p.wins,
      losses: p.losses,
      buchholz: p.buchholz,
    }));
  }

  simulateRound(isDecision) {
    const roundResults = this.rounds[this.rounds.length - 1].map(
      ({ player1, player2 }) => {
        const winner = Math.random() > 0.5 ? player1.name : player2.name;
        const loser = winner === player1.name ? player2.name : player1.name;
        const diff = Math.floor(Math.random() * 10); // Random diff
        return { won: winner, lost: loser, diff };
      }
    );

    if (!isDecision) this.processResults(roundResults);
    else console.log(`-------- Winner ${roundResults[0].won} --------`);
  }

  // Simulate tournament rounds until the end condition is met
  simulateTournament(results) {
    while (!this.checkEndCondition()) {
      this.generateRound();
      this.printRound();
      if (!results) this.simulateRound(false);
      else this.processResults(results[this.rounds.length - 1]);
      console.log(this.generateStandings());
    }

    this.generateDecisionRound();
  }
}
