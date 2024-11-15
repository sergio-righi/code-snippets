class SwissTournament {
  constructor(participants, slots) {
    this.participants = participants;
    this.slots = slots;
    this.rounds = [];
    this.results = [];
    const { breakpoint, slices } = this.getConfiguration(
      this.participants.length
    );
    Object.assign(this, { breakpoint, slices });
  }

  getConfiguration(participants) {
    const breakpoint = Math.ceil(Math.log2(participants)) - 1; // Compute breakpoint
    const fullBracketSize = 2 ** breakpoint; // Closest power of 2 greater than participants
    const difference = fullBracketSize - participants; // Excess spots in the bracket

    const slices = [];
    let remainingParticipants = participants;

    // Generate the growing part of slices
    for (let i = 0; i < breakpoint; i++) {
      const sliceSize = Math.min(remainingParticipants, 2 ** i);
      slices.push(sliceSize);
      remainingParticipants -= sliceSize;
      if (remainingParticipants <= 0) break;
    }

    // Mirror the growing part to create the symmetric slices array
    const mirrored = slices.slice(0, -1).reverse();

    return { breakpoint, slices: slices.concat(mirrored) };
  }

  // Sort participants based on the rules (wins, losses, score, diff)
  sortParticipants() {
    this.participants.sort((a, b) => {
      if (a.wins !== b.wins) return b.wins - a.wins;
      if (a.losses !== b.losses) return a.losses - b.losses;
      if (a.score !== b.score) return b.score - a.score;
      return b.diff - a.diff;
    });
  }

  // Remove participants who have 3 wins or 3 losses
  filterParticipants() {
    return this.participants.filter(
      (p) => p.wins < this.breakpoint && p.losses < this.breakpoint
    );
  }

  sliceArray(array, parts) {
    const chunkSize = Math.ceil(array.length / parts); // Calculate the size of each chunk
    const slices = [];

    for (let i = 0; i < array.length; i += chunkSize) {
      slices.push(array.slice(i, i + chunkSize)); // Slice the array into parts
    }

    return slices;
  }

  printRound() {
    console.log(
      this.rounds[this.rounds.length - 1].map(
        (item) => `${item.player1.name} vs ${item.player2.name}`
      )
    );
  }

  // Generate a new round
  generateRound() {
    this.sortParticipants();
    const participants = this.filterParticipants();
    if (participants.length < 2) return; // If no participants left for pairing, stop.

    console.log(`-------- Round ${this.rounds.length + 1} --------`);
    const round = [];
    const slices = this.sliceArray(
      participants,
      this.slices[this.rounds.length]
    );
    for (let i = 0; i < slices.length; i++) {
      const middle = slices[i].length / 2;
      for (let j = 0; j < middle; j++) {
        round.push({
          player1: slices[i][j],
          player2: slices[i][middle + j],
        });
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

  // Process round results and update participants' stats
  processResults(roundResults) {
    roundResults.forEach((result) => {
      const { won, lost, diff } = result;
      const winner = this.participants.find((p) => p.name === won);
      const loser = this.participants.find((p) => p.name === lost);

      // Update winner's stats
      winner.wins = (winner.wins || 0) + 1;
      winner.score = (winner.score || 0) + (loser.weight - winner.weight);
      winner.diff = (winner.diff || 0) + diff;

      // Update loser's stats
      loser.losses = (loser.losses || 0) + 1;
      loser.score = (loser.score || 0) + (winner.weight - loser.weight);
      loser.diff = (loser.diff || 0) - diff;
    });
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
      rank: index + 1,
      name: p.name,
      wins: p.wins,
      losses: p.losses,
      // score: p.score,
      // diff: p.diff,
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
  simulateTournament() {
    while (!this.checkEndCondition()) {
      this.generateRound();
      this.printRound();
      this.simulateRound(false);
      console.log(this.generateStandings());
    }

    this.generateDecisionRound();

    console.log(this.generateStandings());
  }
}

// Example usage:
const participants = [
  { name: "Ana", weight: 0, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Bob", weight: 1, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Chloe", weight: 2, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Diana", weight: 3, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Eve", weight: 4, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Fran", weight: 5, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Gary", weight: 6, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Helen", weight: 7, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Isabel", weight: 8, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "John", weight: 9, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Kate", weight: 10, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Lucas", weight: 11, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Mavie", weight: 12, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Noa", weight: 13, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Owen", weight: 14, wins: 0, losses: 0, score: 0, diff: 0 },
  { name: "Phil", weight: 15, wins: 0, losses: 0, score: 0, diff: 0 },
];

new SwissTournament(participants, 8).simulateTournament();
