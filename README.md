# Tiny Tapeout datasheet builder

See https://tinytapeout.com for details on the project.

To run the tool locally or have a fork's GitHub action work, you need the GH_USERNAME and GH_TOKEN set in your environment.

GH_USERNAME should be set to your GitHub username.

To generate your GH_TOKEN go to https://github.com/settings/tokens/new . You don't need to tick any boxes in the form, the default is fine.

To run locally, make a file like this:

    export GH_USERNAME=<username>
    export GH_TOKEN=<token>

And then source it before running the tool.

For GitHub actions, go to your fork's settings, choose secrets, then actions. 
Click the 'new repository secret' button and set GH_USERNAME and GH_TOKEN to be your username and the token.

## Making PRs

Please run the ./lint.sh script to lint your modification before making a PR.
