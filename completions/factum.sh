_factum_completion() {
	filename="${1##*/}"
	if [[ "$filename" =~ ^(Factum|.+\.factum)$ ]]; then
		COMP_WORDS=(factotum --path "${COMP_WORDS[0]}" run "${COMP_WORDS[@]:1}")
		COMP_CWORD=$((COMP_CWORD + 3))
		_factotum_completion factotum "$2" "$3"
	else
		return 1
	fi
}

_factum_completion_setup() {
	complete -D -o nosort -F _factum_completion -o bashdefault -o default
}

_factum_completion_setup;
