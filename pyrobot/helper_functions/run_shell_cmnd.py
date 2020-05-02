#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import asyncio
from typing import List


async def run_command(shell_command: List) -> (str, str):
    """ executes a shell_command, 
    and returns the stdout and stderr"""
    process = await asyncio.create_subprocess_exec(
        *shell_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    # Wait for the subprocess to finish
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    return t_response, e_response
