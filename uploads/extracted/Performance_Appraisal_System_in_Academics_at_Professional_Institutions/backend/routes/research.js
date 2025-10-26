const express = require('express');
const ResearchPaper = require('../models/ResearchPaper');
const router = express.Router();

// Get all research papers
router.get('/', async (req, res) => {
    try {
        const papers = await ResearchPaper.find().populate('uploadedBy', 'username');
        res.json(papers);
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
});

// Get single research paper
router.get('/:id', async (req, res) => {
    try {
        const paper = await ResearchPaper.findById(req.params.id).populate('uploadedBy', 'username');
        if (!paper) {
            return res.status(404).json({ message: 'Research paper not found' });
        }
        res.json(paper);
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
});

// Create new research paper
router.post('/', async (req, res) => {
    try {
        const paper = new ResearchPaper(req.body);
        await paper.save();
        res.status(201).json(paper);
    } catch (error) {
        res.status(500).json({ message: 'Server error', error: error.message });
    }
});

module.exports = router;
