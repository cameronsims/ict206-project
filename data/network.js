const options = {
	"configure": {
		"enabled": true,
		"filter": ["interaction", "manipulation", "physics"]
	},
    "physics": {
        "forceAtlas2Based": {
            "springLength": 100,
            "avoidOverlap": 1
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
    }
}